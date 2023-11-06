import openai

# Replace 'YOUR_API_KEY' with your OpenAI API key
api_key = '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'

def chat_with_gpt3(prompt):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a software engineer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print("Welcome to ChatGPT! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("Beckett: ")
        if user_input.lower() == "exit":
            break
        
        response = chat_with_gpt3(user_input)
        print("ChatGPT:", response)
