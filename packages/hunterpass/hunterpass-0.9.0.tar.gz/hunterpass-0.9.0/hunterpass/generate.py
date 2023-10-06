import openai
import os

def get_api_key():
    return os.getenv('OPENAI_API_KEY')

def generate_wordlist(output_file="dictionary.txt"):
    api_key = get_api_key()

    if api_key is None:
        print("Error: API key not found. Please, set OPENAI_API_KEY environment variable.")
        return
    
    num_variations = int(input("Type the number of variations: "))
    min_length = int(input("Type the minimum length of the wordlist: "))
    max_length = int(input("Type the maximum length of the wordlist: "))

    openai.api_key = api_key

    initial_message = f"Generate a wordlist with the following information ({num_variations} variations, min quantity = {min_length} and max quantity {max_length}). Make combinations and mix the informations:\n"

    user_input = []

    while True:
        information = input("Type a information for wordlist (Type 'exit' to quit): ").lower()
        if information.lower() == 'exit':
            break
        user_input.append(information)

    initial_message += "\n".join([f"Information: {info}" for info in user_input])

    messages = [{"role": "user", "content": initial_message}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    generated_text = response.choices[0].message['content'].strip()

    with open(output_file, 'w') as f:
        f.write(generated_text)

if __name__ == "__main__":
    generate_wordlist()