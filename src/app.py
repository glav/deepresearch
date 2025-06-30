from dotenv import load_dotenv
import os
from load_env import load_env
from openai import OpenAI

def main():
    # Load environment variables from .env files
    load_env()


    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        input="Write a one-sentence bedtime story about a unicorn."
    )

    print(response.output_text)

if __name__ == "__main__":
    main()
