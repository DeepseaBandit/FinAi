from flask import Flask, render_template, jsonify, request
import pandas as pd
from langchain_together import Together

app = Flask(__name__)

# Initialize the Together AI model
def initialize_llm():
    return Together(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        together_api_key="tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE",
        max_tokens=30000
    )

# Function to clean the output from Together AI
def get_cleaned_output(prompt, llm):
    result = llm.invoke(prompt)
    # Split by lines, remove the first 2 lines, and join the rest
    cleaned_result = "\n".join(result.splitlines()[3:])
    return cleaned_result

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/get_analysis", methods=["POST"])
def get_analysis():
    try:
        feature = request.json.get('feature')
        
        # Read the CSV file
        try:
            df = pd.read_csv("AdaniGreen.csv", usecols=[0, 1])
            article_text = df
        except FileNotFoundError:
            # If file not found, use sample data
            article_text = "Sample financial data for demonstration"
            
        llm = initialize_llm()
        
        # Generate different prompts based on the requested feature
        if feature == 'dataAnalysis':
            prompt = f"""Analyze the financial data provided and generate a detailed analysis, focusing on trends, patterns, and key financial insights without explicitly describing the given values. Additionally, forecast 'Your Company’s' future financial performance by identifying trends, patterns, and key indicators to predict potential growth, profitability, and market position. Consider historical performance, industry benchmarks, and economic factors while making data-driven projections. Conclude with a concise evaluation of 'Your Company’s' financial health and expected trajectory, replacing 'the company' with 'Your Company' in the summary. Ensure the analysis is insightful, forward-looking, and based on clear data-driven reasoning. Write in 150 words:  {article_text}"""
        if feature == 'budgeting':
            prompt = f"""Analyze the financial data provided and generate a detailed budgeting report for 'Your Company.' Identify key revenue streams, fixed and variable costs, operational expenses, and profitability margins. Assess cash flow trends, cost efficiency, and potential areas for financial optimization. Provide a breakdown of expected expenditures, investment allocations, and projected savings. Conclude with a concise evaluation of 'Your Company’s' financial planning, ensuring sustainable growth and stability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"""
        if feature == 'expenseManagement':
            prompt = f"""Analyze the financial data provided and generate a detailed expense management report for 'Your Company.' Identify key fixed and variable costs, operational expenses, and cash flow trends. Assess cost efficiency, highlight areas of excessive spending, and suggest strategies for optimization. Provide insights into budgeting, cost-cutting opportunities, and resource allocation to enhance profitability. Conclude with a concise evaluation of 'Your Company's' expense management strategy, ensuring financial stability and long-term sustainability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"""
        if feature == 'investment':
            prompt = f"""Based on the financial data provided, recommend investment strategies for 'Your Company'. Suggest potential areas for capital allocation, growth opportunities, and risk management considerations. Include both short-term and long-term investment perspectives in your recommendations. Write in a clear, professional manner with actionable advice in about 150 words:  {article_text}"""
        # else:
        #     prompt = f"""Based on the financial data provided, give a general analysis of 'Your Company's' financial position and offer relevant recommendations. Write in a professional but approachable manner in about 150 words:  {article_text}"""

        result = get_cleaned_output(prompt, llm)
        return jsonify({"success": True, "result": result})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '')
    
    # Call your existing chatbot implementation
    response = generate_chatbot_response(user_message)
    
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)