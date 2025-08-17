import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "")

def ask_llm(prompt, user_input, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
