import openai
import os

def get_api_key():
    return os.getenv('OPENAI_API_KEY')

def get_user_input():
    user_input = []

    while True:
        information = input("Type a information for wordlist (Type 'exit' to quit): ").lower()
        if information.lower() == 'exit':
            break
        user_input.append(information)

    return user_input

def generate_wordlist(output_file="dictionary.txt"):
    api_key = get_api_key()

    if api_key is None:
        print("Error: API key not found. Please, set OPENAI_API_KEY environment variable.")
        return

    user_input = get_user_input()

    openai.api_key = api_key

    prompt = "Generate a wordlist with:\n"
    for info in user_input:
        prompt += f"Information: {info}\n"
    
    response = openai.Completion.create(
        engine="davinci", 
        prompt=prompt, 
        max_tokens=2048
    )
    
    generated_text = response.choices[0].text.strip()

    with open(output_file, 'w') as f:
        f.write(generated_text)

if __name__ == "__main__":
    generate_wordlist()