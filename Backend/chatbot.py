import requests

API_KEY = "tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE"
API_URL = "https://api.together.xyz/v1/chat/completions"

def chat_with_ai(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",  # Choose a model from Together AI
        "messages": [{"role": "system", "content": "You are a helpful chatbot."},
                     {"role": "user", "content": user_input}],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

# Chat loop
while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        break
    response = chat_with_ai(user_message)
    print("Bot:", response)
