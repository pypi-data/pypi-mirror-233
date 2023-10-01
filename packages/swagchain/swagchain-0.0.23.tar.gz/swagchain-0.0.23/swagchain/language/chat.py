from typing import (AsyncGenerator, Dict, List, Literal, Optional, TypeAlias,
                    TypeVar)

import openai  # pylint-disable=E0401
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")

Role: TypeAlias = Literal["assistant", "user", "system", "function"]
Model: TypeAlias = Literal["gpt-4-0613", "gpt-3.5-turbo-16k-0613"]
Size: TypeAlias = Literal["256x256", "512x512", "1024x1024"]
Format: TypeAlias = Literal["url", "base64"]


class Message(BaseModel):
    """
    A message in a chat

    Args:
            role (Role): The role of the message (assistant, user, system, function)
            content (str): The content of the message
    """

    role: Role = Field(..., description="The role of the message")
    content: str = Field(..., description="The content of the message")


class ChatCompletionRequest(BaseModel):
    """

    Chat completion request

    Args:

            model (Model): The model to use for the completion (gpt-4-0613, gpt-3.5-turbo-16k-0613)
            messages (List[Message]): The messages to use for the completion
            temperature (float): The temperature of the completion
            max_tokens (int): The maximum number of tokens to generate
            stream (bool): Whether to stream the completion or not
    """

    model: Model = Field(..., description="The model to use for the completion")
    messages: List[Message] = Field(
        ..., description="The messages to use for the completion"
    )
    temperature: float = Field(
        default=0.5, description="The temperature of the completion"
    )
    max_tokens: int = Field(
        1024, description="The maximum number of tokens to generate"
    )
    stream: bool = Field(False, description="Whether to stream the completion or not")


class ChatCompletionUssage(BaseModel):
    """

    Chat completion usage

    Args:

            prompt_tokens (int): The number of tokens in the prompt

            completion_tokens (int): The number of tokens in the completion

            total_tokens (int): The total number of tokens

    """

    prompt_tokens: int = Field(..., description="The number of tokens in the prompt")
    completion_tokens: int = Field(
        ..., description="The number of tokens in the completion"
    )
    total_tokens: int = Field(..., description="The total number of tokens")


class ChatCompletionChoice(BaseModel):
    """

    Chat completion choice

    Args:

            index (int): The index of the choice

            message (Message): The message of the choice

            finish_reason (str): The reason the choice was finished

    """

    index: int = Field(..., description="The index of the choice")
    message: Message = Field(..., description="The message of the choice")
    finish_reason: str = Field(..., description="The reason the choice was finished")


class ChatCompletionResponse(BaseModel):
    """

    Chat completion response

    Args:

            id (str): The id of the completion

            object (str): The object of the completion

            created (int): The creation time of the completion

            model (Model): The model used for the completion

            choices (List[ChatCompletionChoice]): The choices of the completion

            usage (ChatCompletionUssage): The usage of the completion

            stream (bool): Whether the completion was streamed or not

    """

    id: str = Field(..., description="The id of the completion")
    object: str = Field(..., description="The object of the completion")
    created: int = Field(..., description="The creation time of the completion")
    model: Model = Field(..., description="The model used for the completion")
    choices: List[ChatCompletionChoice] = Field(
        ..., description="The choices of the completion"
    )
    usage: ChatCompletionUssage = Field(..., description="The usage of the completion")
    stream: bool = Field(..., description="Whether the completion was streamed or not")


class VectorResponse(BaseModel):
    """

    Vector response

    Args:

            id (str): The id of the vector

            object (str): The object of the vector

            created (int): The creation time of the vector

            model (Model): The model used for the vector

            data (List[float]): The data of the vector

    """

    text: str = Field(..., description="The text of the completion")
    score: float = Field(..., description="The score of the completion")


class CreateImageResponse(BaseModel):
    """

    Create image response

    Args:

            id (str): The id of the image

            object (str): The object of the image

            created (float): The creation time of the image

            data (List[Dict[Format, str]]): The data of the image

    """

    created: float = Field(...)
    data: List[Dict[Format, str]] = Field(...)


class CreateImageRequest(BaseModel):
    """

    Create image request

    Args:

            prompt (str): The prompt of the image

            n (int): The number of images to generate

            size (Size): The size of the image

            response_format (Format): The format of the response

    """

    prompt: str = Field(...)
    n: int = Field(default=1)
    size: Size = Field(default="1024x1024")
    response_format: Format = Field(default="url")


class LanguageModel(BaseModel):
    """

    ChatGPT: A GPT-3.5+ chatbot

    This class represents ChatGPT Large Language Model behavior and is a wrapper around the OpenAI Chat API.

    Args:

            model (Model): The model to use for the completion (gpt-4-0613, gpt-3.5-turbo-16k-0613)

            temperature (float): The temperature of the completion

            max_tokens (int): The maximum number of tokens to generate

    """

    model: Model = Field(default="gpt-3.5-turbo-16k-0613")
    temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=1024)

    async def chat(self, text: str, context: Optional[str] = None) -> str:
        """

        Chat with the bot with the option to pass a context

        Args:

                text (str): The text to send to the bot

                context (Optional[str], optional): The context of the bot. Defaults to None.

        Returns:

                str: The response of the bot

        """

        if context is not None:
            messages = [
                Message(role="user", content=text).dict(),
                Message(role="system", content=context).dict(),
            ]
        else:
            messages = [Message(role="user", content=text).dict()]

        response = await openai.ChatCompletion.acreate(  # type: ignore
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=False,
        )

        return response.choices[0].message.content  # type: ignore

    async def assist(self, text: str) -> str:
        """
        Assistance with `gpt-3.5-turbo-instruct` model. Similar to `text-davinci` but with more focus on instructions and state of the GPT3.5 model.

        Args:

                text (str): The text to send to the bot

        Returns:

                str: The response of the bot

        """
        response = await openai.Completion.acreate(  # type: ignore
            model="gpt-3.5-turbo-instruct",
            prompt=text,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=False,
        )
        return response.choices[0].text  # type: ignore

    async def stream(
        self, text: str, context: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        The chat between the bot and the user is streamed through an async generator, suitable for websockets and server-sent events

        Args:

                text (str): The text to send to the bot

                context (Optional[str], optional): The context of the bot. Defaults to None.

        Yields:

                AsyncGenerator[str, None]: The response of the bot

        """

        if context is not None:
            messages = [
                Message(role="user", content=text).dict(),
                Message(role="system", content=context).dict(),
            ]
        else:
            messages = [Message(role="user", content=text).dict()]

        response = await openai.ChatCompletion.acreate(  # type: ignore
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,
        )

        async for message in response:  # type: ignore
            data = message["choices"][0]["delta"].get("content")  # type: ignore
            if data is not None:
                yield data
            else:
                break


    async def image(self, text: str, n: int = 1, size: Size = "1024x1024", response_format: Format = "url") ->str:
        """
        Generate images from text

        Args:

                text (str): The text to generate from

                n (int, optional): The number of images to generate. Defaults to 1.

                size (Size, optional): The size of the image. Defaults to "1024x1024".

                response_format (Format, optional): The format of the response. Defaults to "url".

        Returns:

                List[Dict[Format, str]]: The data of the images

        """
        response = await openai.Image.acreate(  # type: ignore
            prompt=text,
            model=self.model,
            n=n,
            size=size,
            response_format=response_format,
        )
        return response['data'][0]['url'] # type: ignore