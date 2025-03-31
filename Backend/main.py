import pandas as pd
import requests
from langchain_together import Together

df = pd.read_csv("AdaniGreen.csv",usecols=[0, 1])
#print(df)  

llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    together_api_key="tgp_v1_49vWGNGcLixzfeMiS8GQNCKg5MH4Wo0sprjba0xhjjE",
    max_tokens= 30000
    
)
article_text = df

prompt1 = f"Analyze the financial data provided and generate a detailed data analysis. Focus on trends, patterns, and key financial insights without explicitly describing the given values. Conclude with a concise evaluation of 'Your Company’s' financial health, replacing 'the company' with 'Your Company' in the summary. Use clear and data-driven reasoning in your conclusion.Write in 150 words: {article_text}"
print(llm.invoke(prompt1))