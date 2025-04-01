import os
import pandas as pd
import json
from flask import Flask, request, jsonify
from langchain_together import Together

# Flask app initialization
app = Flask(__name__)

# Load financial data
df = pd.read_csv("AdaniGreen.csv", usecols=[0, 1])

# Initialize LangChain Together API with the direct API key in the code
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    together_api_key="tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE",  # API Key directly in the code
    max_tokens=30000
)

<<<<<<< HEAD
print("BUDGETING REPORT")
prompt2 = f"Analyze the financial data provided and generate a detailed budgeting report for 'Your Company.' Identify key revenue streams, fixed and variable costs, operational expenses, and profitability margins. Assess cash flow trends, cost efficiency, and potential areas for financial optimization. Provide a breakdown of expected expenditures, investment allocations, and projected savings. Conclude with a concise evaluation of 'Your Company’s' financial planning, ensuring sustainable growth and stability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"
print(llm.invoke(prompt2))
=======
# Define prompts for each feature
PROMPTS = {
    "data-analysis": f"Analyze the financial data provided and generate a detailed analysis, focusing on trends, patterns, and key financial insights without explicitly describing the given values. Additionally, forecast 'Your Company’s' future financial performance by identifying trends, patterns, and key indicators to predict potential growth, profitability, and market position. Consider historical performance, industry benchmarks, and economic factors while making data-driven projections. Conclude with a concise evaluation of 'Your Company’s' financial health and expected trajectory. Use 150 words: {df}",
    
    "budgeting": f"Analyze the financial data provided and generate a detailed budgeting report for 'Your Company.' Identify key revenue streams, fixed and variable costs, operational expenses, and profitability margins. Assess cash flow trends, cost efficiency, and potential areas for financial optimization. Provide a breakdown of expected expenditures, investment allocations, and projected savings. Conclude with a concise evaluation of 'Your Company’s' financial planning, ensuring sustainable growth and stability. Use 150 words: {df}",
    
    "expense-management": f"Analyze the financial data provided and generate a detailed expense management report for 'Your Company.' Identify key fixed and variable costs, operational expenses, and cash flow trends. Assess cost efficiency, highlight areas of excessive spending, and suggest strategies for optimization. Provide insights into budgeting, cost-cutting opportunities, and resource allocation to enhance profitability. Conclude with a concise evaluation of 'Your Company's' expense management strategy. Use 150 words: {df}",
    
    "investment": f"Analyze the financial data provided and generate an investment strategy for 'Your Company.' Identify key investment opportunities, potential risks, and market trends. Assess financial growth potential, ROI, and industry benchmarks. Provide recommendations on optimizing investment strategies and asset allocation for long-term profitability. Conclude with a concise evaluation of 'Your Company’s' investment outlook. Use 150 words: {df}",
    
    "chatbot": f"Provide a general financial consultation based on the given data. Identify financial strengths, weaknesses, and opportunities for improvement. Provide insights into budgeting, investing, and cost management based on industry best practices. Use 150 words: {df}"
}

@app.route("/analyze-metric", methods=["POST"])
def analyze_metric():
    try:
        data = request.json
        feature = data.get("feature")
>>>>>>> 27f29530ce074e4dd2d8bdb92bb7a39070c1e4b1

        # Validate feature type
        if feature not in PROMPTS:
            return jsonify({"error": "Invalid feature selected"}), 400

        # Generate AI response
        response = llm.invoke(PROMPTS[feature])

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)