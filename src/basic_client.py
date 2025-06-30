from openai import OpenAI

def do_basic_completion():
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        input="Write a one-sentence bedtime story about a unicorn."
    )

    print(response.output_text)
