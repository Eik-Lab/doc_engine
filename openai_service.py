import openai
from templates import system_roles
import streamlit as st


# Define the function to generate text using OpenAI API
def generate_text(
    system_role,
    user_input: str,
    temperature=0.7,
    max_words=150,
):
    # Set the maximum number of tokens
    openai.api_key = st.session_state.api_key
    tokens_per_word = 15
    max_tokens = max_words * tokens_per_word

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # use the gpt-3.5-turbo
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": system_role,
            },  # add the start sequence as the first message
            {
                "role": "user",
                "content": user_input,
            },  # add the prompt as the second message
        ],
        temperature=temperature,  # set the temperature
    )

    return response["choices"][0]["message"]["content"]  # return the generated text
