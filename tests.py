import os
from openai import OpenAI

client = OpenAI(
    api_key='sk-proj-PvEfnv5D8WVXEGc6W1coT3BlbkFJZi45uBOmKi31jtE4QrGv'
)

def chat_with_gpt():
    print("ChatGPT - Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
            )
            print("ChatGPT:", response.choices[0].message)
        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    chat_with_gpt()
