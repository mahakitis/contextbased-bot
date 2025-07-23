import os
from groq import Groq
from dotenv import load_dotenv
from .prompts import build_prompt, build_rephrase_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rephrase_question(current_question, previous_question=None):
    prompt = build_rephrase_prompt(current_question, previous_question)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You rephrase User questions that can also be vague or follow-up questions into complete standalone questions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
        max_tokens=512
    )
    return response.choices[0].message.content.strip()


def generate_answer(question, context):
    prompt = build_prompt(question, context)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that only answers based on the provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=512
    )
    return response.choices[0].message.content.strip()
