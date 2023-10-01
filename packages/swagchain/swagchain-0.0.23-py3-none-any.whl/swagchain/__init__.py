from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Generic, Iterator, Set, Type, TypeAlias, TypeVar

from aiohttp import ClientSession
from jinja2 import Template
from langchain.agents.agent_toolkits.openapi import planner
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.requests import RequestsWrapper

from .aws import *
from .database import *
from .lib import *
from .tools import *

MessagePromptMapping: TypeAlias = Dict[str,Role]

MESSAGE_TO_PROMPT_MAPPING:MessagePromptMapping = {
    "HumanMessage": "user",
	"SystemMessage": "system",
	"AIMessage": "assistant"
}


class Agent(BaseModel, ABC):
    llm: LanguageModel = Field(default_factory=LanguageModel)
    memory: Memory = Field(default_factory=Memory)
    namespace: str
    topK: int
    template_str: str
    
    def __hash__(self):
        return hash((self.namespace, self.topK))

    def __eq__(self, other:object)->bool:
        if not isinstance(other, type(self)): return False
        return (self.namespace, self.topK) == (other.namespace, other.topK)
    
    @property
    def tools(self)->Set[Type[OpenAIFunction]]:
        """
        Get the tools of the agent
        """
        return OpenAIFunction.Metadata.subclasses




    @abstractmethod
    async def chain(self, text: str, **kwargs:Any) -> str:
        """
        Chain a text
        """
        ...

    
    @retry()
    @handle_errors
    @process_time
    async def assist(self, text: str) -> str:
        """
        Assist with GPT-3.5 instructions
        ----------------------

        Args:

                text (str): The text to assist with

        Returns:

                str: The generated text

        The agent will call the GPT-3.5 instruction completion API
        """

        return await self.llm.assist(text=text)
    
    @property
    def actions(self) -> List[str]:
        """
        Get the actions of the agent
        """
        return [name for name, _ in inspect.getmembers(self.__class__, inspect.isfunction) if not name.startswith("_")]




class Swagchain(Agent):
    """
    Swagchain: A retrieval augmented generation agent
    ----------------------

    This class is a wrapper around the OpenAI Chat API, Pinecone Emedding and DynamoDB Message History. It streamlines the process of creating a retrieval augmented generation agent.
    """

    llm: LanguageModel = Field(default_factory=LanguageModel)
    memory: Memory = Field(default_factory=Memory)
    namespace: str = Field(...)
    topK: int = Field(default=10)
    template_str: str = Field(...)

    @property
    def history(self) -> DynamoDBChatMessageHistory:
        return DynamoDBChatMessageHistory(
            table_name=self.__class__.__name__, session_id=self.namespace
        )
    
    @property
    def tools(self)->Set[Type[OpenAIFunction]]:
        """
        Get the tools of the agent
        """
        return OpenAIFunction.Metadata.subclasses
    
    @handle_errors
    @async_io
    def fetch(self) -> List[Message]:
        """
        Get messages from the history
        ----------------------

        Args:

                prompt (str): The prompt to get messages from

        Returns:

                List[Message]: The messages
        """
        messages = self.history.messages
        return [ Message(role=MESSAGE_TO_PROMPT_MAPPING[message.__class__.__name__], content=message.content) for message in messages]  
    
    @handle_errors
    @async_io
    def add_ai_message(self, text: str) -> None:
        """
        Add an AI message to the history
        ----------------------

        Args:

                text (str): The text to add
        """
        self.history.add_ai_message(text)
    
    @handle_errors
    @async_io
    def add_user_message(self, text: str) -> None:
        """
        Add a user message to the history
        ----------------------

        Args:

                text (str): The text to add
        """
        self.history.add_user_message(text)

    @retry()
    @handle_errors
    @process_time
    async def chain(self, text: str, **kwargs:Any) -> str:
        """
        Retrieval Augmented Generation
        ----------------------

        Args:

                text (str): The text to retrieve from

        Returns:

                str: The generated text

        The agent will find for the KNN of the text into his memory namespace and generate from them
        a response
        """

        knn = await self.memory.search(
            text=text, namespace=self.namespace, top_k=self.topK
        )
        logger.info(knn)
        logger.info(self.namespace)
        if len(knn) == 0:
            response = await self.llm.chat(text=text)
        else:
            context = await Template(self.template_str, enable_async=True).render_async(suggestions=knn, **kwargs)
            response = await self.llm.chat(text=text, context=context)
        await self.memory.save(texts=[text, response], namespace=self.namespace)
        return response


    async def stream_chain(self, text: str) -> AsyncGenerator[str, None]:
        """
        Retrieval Augmented Generation (stream)
        ----------------------

        Args:

                text (str): The text to retrieve from

        Returns:

                AsyncGenerator[str, None]: The generated text

        The agent will find for the KNN of the text into his memory namespace and generate from them
        a response
        """
         
        full_response = ""
        knn = await self.memory.search(
            text=text, namespace=self.namespace, top_k=self.topK
        )
        if len(knn) == 0:
            async for response in self.llm.stream(text=text):
                full_response += response
                yield response
        else:
            context = await Template(self.template_str, enable_async=True).render_async(suggestions=knn)
            logger.info(context)
            async for response in self.llm.stream(text=text, context=context):
                full_response += response
                yield response
        await self.memory.save(texts=[text, full_response], namespace=self.namespace)
        await self.add_user_message(text)  
        await self.add_ai_message(full_response)

    
    @retry()
    @handle_errors
    @process_time
    async def plugin(self, url:str,text:str)->str:
        """
        OpenAPI Plugin
        ----------------------
        The agent retrieves and reduces the openapi spec of the url and creates an agent executor from it, then runs the user's text query through it
        """
        async with ClientSession() as session:
            response = await session.get(url+"/openapi.json")
            spec = await response.json()
            reduced_spec = reduce_openapi_spec(spec)
            agent_executor = planner.create_openapi_agent(api_spec=reduced_spec, requests_wrapper=RequestsWrapper(aiosession=session),llm=ChatOpenAI())
            return await agent_executor.arun(text)

    @retry()
    @handle_errors
    @process_time
    @async_io
    def create_table(self) -> None:
        """
        Create the table
        ----------------------
        The agent creates the table in DynamoDB
        """
        from boto3 import client
        dynamodb = client("dynamodb")
        dynamodb.create_table(
            TableName=self.__class__.__name__,
            KeySchema=[
                {"AttributeName": "SessionId", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "SessionId", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        dynamodb.get_waiter("table_exists").wait(TableName=self.__class__.__name__)
             
A = TypeVar("A", bound=Agent)
S = TypeVar("S", bound=Swagchain)

class AgentSwarm(ABC, Generic[A]):
    def __init__(self, agents: Set[A]) -> None:
        self.agents = agents


    def __iter__(self) -> Iterator[A]:
        return iter(self.agents)
    

    def __getitem__(self, name: str) -> A:
        for agent in self.agents:
            if agent.__class__.__name__ == name:
                return agent
        raise KeyError(f"Agent {name} not found")
    
    def __repr__(self) -> str:
        return f"AgentGroup({' '.join([agent.__class__.__name__ for agent in self.agents])})"
    
    def __len__(self) -> int:
        return len(self.agents)
    
    def __contains__(self, name: str) -> bool:
        return name in [agent.__class__.__name__ for agent in self.agents]
    
    def __add__(self, other: A) -> AgentSwarm[A]:
        self.agents.add(other)
        return self
    
    def __sub__(self, other: A) -> AgentSwarm[A]:
        self.agents.remove(other)
        return self
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, AgentSwarm):
            return self.agents == other.agents # type: ignore
        return False
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return hash(self.agents)
    
    @property
    @abstractmethod
    def commander(self) -> A:
        """
        Get the commander of the group
        """
        ...

    @abstractmethod
    async def broadcast(self, text: str) -> List[str]:
        """
        Broadcast a text to all the agents
        """
        ...

    @abstractmethod 
    async def ask(self, text: str, agent: str) -> str:
        """
        Ask a specific agent
        """
        ...

    @abstractmethod
    async def tell(self, text: str, agent: Optional[str]=None) -> str:
        """
        Tell a specific agent
        """
        ...


class SwagchainGroup(AgentSwarm[S]):
    async def broadcast(self, text: str) -> List[str]:
        """
        Broadcast a text to all the agents
        """
        return await asyncio.gather(*[agent.chain(text=text) for agent in self.agents])
    
    async def ask(self, text: str, agent: str) -> str:
        """
        Ask a specific agent
        """
        _agent = self[agent]
        return await _agent.chain(text=text)
    
    async def tell(self, text: str, agent: Optional[str]=None) -> str:
        """
        Tell a specific agent
        """
        if agent is None:
            return await self.commander.chain(text=text)
        _agent = self[agent]
        return await _agent.chain(text=text)
    

    @property
    def commander(self) -> S:
        """
        Get the commander of the group
        """
        return sorted(self.agents, key=lambda agent: agent.topK, reverse=True)[0]