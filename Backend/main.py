from flask import Flask, request, jsonify
import os
from langchain_together import Together

app = Flask(__name__)

# Initialize the AI model using environment variable for the API key
api_key = os.getenv("TOGETHER_API_KEY")  # Store your API key securely in environment variables
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    together_api_key='tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE',
    max_tokens=30000
)

# Define the prompts for each feature
prompts = {
    1: "Analyze the financial data provided and generate a detailed analysis, focusing on trends, patterns, and key financial insights. Additionally, forecast future financial performance.",
    2: "Generate a detailed budgeting report for the company, identifying revenue streams, expenses, and cost optimization strategies.",
    3: "Analyze the expense management strategy, focusing on cost efficiency, budgeting, and expense allocation.",
    4: "Provide an investment analysis report, evaluating potential growth and opportunities based on current financial data.",
    5: "Provide an AI chatbot feature for answering financial queries, offering insights on financial data and providing recommendations."
}

@app.route('/api/process-prompt', methods=['POST'])
def process_prompt():
    try:
        # Get the prompt number from the frontend request
        data = request.get_json()
        prompt_number = data.get("prompt_number")

        # Validate the prompt number
        if prompt_number not in prompts:
            return jsonify({"response": "Invalid prompt number."}), 400

        # Get the prompt text based on the prompt number
        prompt_text = prompts[prompt_number]

        # Call the AI model to generate the response
        ai_response = llm.invoke(prompt_text)

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)