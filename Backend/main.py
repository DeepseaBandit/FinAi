import pandas as pd
from langchain_together import Together

df = pd.read_csv("AdaniGreen.csv", usecols=[0, 1])

llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    together_api_key="tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE",
    max_tokens=30000
)

article_text = df

def get_cleaned_output(prompt):
    result = llm.invoke(prompt)
    # Split by lines, remove the first 2 lines, and join the rest
    cleaned_result = "\n".join(result.splitlines()[3:])
    return cleaned_result

print("DATA ANALYSIS & FORECAST")
prompt1 = f"""Analyze the financial data provided and generate a detailed analysis, focusing on trends, patterns, and key financial insights without explicitly describing the given values. Additionally, forecast 'Your Company’s' future financial performance by identifying trends, patterns, and key indicators to predict potential growth, profitability, and market position. Consider historical performance, industry benchmarks, and economic factors while making data-driven projections. Conclude with a concise evaluation of 'Your Company’s' financial health and expected trajectory, replacing 'the company' with 'Your Company' in the summary. Ensure the analysis is insightful, forward-looking, and based on clear data-driven reasoning. Write in 150 words:  {article_text}"""
print(get_cleaned_output(prompt1))

print("BUDGETING REPORT")
prompt2 = f"""Analyze the financial data provided and generate a detailed budgeting report for 'Your Company.' Identify key revenue streams, fixed and variable costs, operational expenses, and profitability margins. Assess cash flow trends, cost efficiency, and potential areas for financial optimization. Provide a breakdown of expected expenditures, investment allocations, and projected savings. Conclude with a concise evaluation of 'Your Company’s' financial planning, ensuring sustainable growth and stability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"""
print(get_cleaned_output(prompt2))

print("EXPENSE MANAGEMENT")
prompt3 = f"""Analyze the financial data provided and generate a detailed expense management report for 'Your Company.' Identify key fixed and variable costs, operational expenses, and cash flow trends. Assess cost efficiency, highlight areas of excessive spending, and suggest strategies for optimization. Provide insights into budgeting, cost-cutting opportunities, and resource allocation to enhance profitability. Conclude with a concise evaluation of 'Your Company's' expense management strategy, ensuring financial stability and long-term sustainability. Replace 'the company' with 'Your Company' in the summary. Use data-driven insights and industry benchmarks to support the analysis. Write in 150 words: {article_text}"""
print(get_cleaned_output(prompt3))
