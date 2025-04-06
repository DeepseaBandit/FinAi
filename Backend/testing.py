from flask import Flask, render_template, request, jsonify
import pandas as pd
from langchain_together import Together
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize Together AI
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    together_api_key="tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE",
    max_tokens=30000
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    analysis_type = data.get('type')
    
    df = pd.read_csv("AdaniGreen.csv", usecols=[0, 1])
    article_text = df
    
    if analysis_type == 'dataAnalysis':
        prompt = f"Analyze the financial data provided and generate a detailed analysis, focusing on trends, patterns, and key financial insights without explicitly describing the given values. Additionally, forecast 'Your Company’s' future financial performance by identifying trends, patterns, and key indicators to predict potential growth, profitability, and market position. Consider historical performance, industry benchmarks, and economic factors while making data-driven projections. Conclude with a concise evaluation of 'Your Company’s' financial health and expected trajectory, replacing 'the company' with 'Your Company' in the summary. Ensure the analysis is insightful, forward-looking, and based on clear data-driven reasoning. Write in 150 words:  {article_text}"  # Your full prompt1
    elif analysis_type == 'budgeting':
        prompt = f"Analyze the financial data provided and generate a detailed budgeting report for 'Your Company.' Identify key revenue streams, fixed and variable costs, operational expenses, and profitability margins. Assess cash flow trends, cost efficiency, and potential areas for financial optimization. Provide a breakdown of expected expenditures, investment allocations, and projected savings. Conclude with a concise evaluation of 'Your Company’s' financial planning, ensuring sustainable growth and stability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"  # Your full prompt2
    elif analysis_type == 'expenseManagement':
        prompt = f"Analyze the financial data provided and generate a detailed expense management report for 'Your Company.' Identify key fixed and variable costs, operational expenses, and cash flow trends. Assess cost efficiency, highlight areas of excessive spending, and suggest strategies for optimization. Provide insights into budgeting, cost-cutting opportunities, and resource allocation to enhance profitability. Conclude with a concise evaluation of 'Your Company's' expense management strategy, ensuring financial stability and long-term sustainability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"  # Your full prompt3
    else:
        return jsonify({"error": "Invalid analysis type"}), 400
    
    result = llm.invoke(prompt)
    return jsonify({"result": result})
API_KEY = "tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE"
API_URL = "https://api.together.xyz/v1/chat/completions"

@app.route('/api/chat', methods=['POST'])
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
while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        break
    response = chat_with_ai(user_message)
    print("Bot:", response)

if __name__ == '__main__':
    app.run(debug=True)