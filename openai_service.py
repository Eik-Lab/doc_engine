import openai

# Set OpenAI API key
openai.api_key = "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"

# Define the function to generate text using OpenAI API
def generate_text(prompt, temperature=0.7, max_words=100):
    start_sequence = "From the info above produce a professional-grade text with an emphasis on providing valuable insights and actionable information. Maintain a professional tone throughout the text, adhering to established conventions for clarity and accuracy."
    prompt = f"{start_sequence}\n{prompt}"

    # Set the maximum number of tokens
    tokens_per_word = 15
    max_tokens = max_words * tokens_per_word

    # Generate text using the Davinci engine
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()
