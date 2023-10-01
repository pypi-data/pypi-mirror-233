from typing import List

import openai

from .vector import *


class Memory(VectorClient):
    """

    Represents Agent's memory
    -------------------------

    Pinecone and OpenAI Embeddings provide the tools needed to build a memory for the agent, this class is a wrapper around them and provides a simple interface to perform similarity search and save new embeddings

    """

    @property
    def builder(self):
        """

        Returns:

            QueryBuilder: A query builder object


        QueryBuilder

        ------------

        A query builder object is a pythonic way to perform queries with MongoDB-like syntax, which is indeed the query language used by Pinecone for it's metadata filtering system.

        https://docs.pinecone.io/reference/query

        """
        return QueryBuilder()

    async def encode(self, texts: List[str], namespace: str) -> List[Embedding]:
        """
        Transforms a list of texts into vectorial embedding objects
        An embedding object is a vector with metadata that is a Key-Value dictionary, where the keys are strings and the values can be `str`, `int`, `float`, `bool` or `list[str]`, useful to store structured data about the text for further filtering and querying.

        Args:

            texts (List[str]): The list of texts to encode

            namespace (str): The namespace of the embeddings

        Returns:

            List[Embedding]: The list of embeddings

        """
        response = await openai.Embedding.acreate(  # type: ignore
            input=texts, model="text-embedding-ada-002"
        )
        response = await openai.Embedding.acreate(
            model="text-embedding-ada-002",
            input=texts,
        )
        data = response["data"]
        return [
            Embedding(
                values=embedding["embedding"],
                metadata={"namespace": namespace, "text": text},
            )
            for embedding, text in zip(data, texts)
        ]

    async def save(self, texts: List[str], namespace: str) -> int:
        """

        Saves a list of texts into the memory

        Args:

            texts (List[str]): The list of texts to save

            namespace (str): The namespace of the embeddings

        Returns:

            int: The number of embeddings saved

        """

        embeddings = await self.encode(texts=texts, namespace=namespace)
        return (await self.upsert(embeddings=embeddings)).upsertedCount

    async def search(self, text: str, namespace: str, top_k: int) -> List[str]:
        """


        Performs a similarity search into the memory

        Args:

            text (str): The text to search

            namespace (str): The namespace of the embeddings

            top_k (int): The number of results to return

        Returns:

            List[str]: The list of results

        """

        embeddings = await self.encode(texts=[text], namespace=namespace)
        expr = (self.builder("namespace") == namespace) & (self.builder("text") != text)
        response = await self.query(
            expr=expr.query,
            vector=embeddings[0].values,
            topK=top_k,
        )
        return [match.metadata["text"] for match in response.matches]  # type: ignore
