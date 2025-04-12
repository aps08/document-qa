"""
This module provides utility functions for generating embeddings using the OpenAI API.
It allows users to generate vector embeddings for a given text using a specified model.
"""

from typing import List, Tuple
from openai import OpenAI
from config import config

client = OpenAI()


def get_vector(*, text: str) -> Tuple[List[float], int]:
    """
    Generates a vector embedding for the given text using the specified OpenAI model.

    Args:
        text (str): The input text for which the embedding is to be generated.

    Returns:
        List[float]: The embedding vector for the input text.
        int: The total number of tokens used in the request.
    """
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding, response.usage.total_tokens


def chat_completion(
    *, context: str, system_message: str, question: str, max_tokens: int, model: str
) -> Tuple[str, str, int]:
    system_message += "If data is found inside the document also mention the page number from which the response is provided. In case relevant data is not found. Say 'Document doesn't contain enough data.'"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        max_tokens=max_tokens,
    )
    completion_id = completion.id
    usage = completion.usage.completion_tokens
    assistant_response = completion.choices[0].message.content
    return assistant_response, completion_id, usage
