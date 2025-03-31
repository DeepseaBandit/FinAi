import pandas as pd
import requests
import openpyxl

from langchain_together import Together

df = pd.read_excel("AdaniGreen.xlsx", engine="openpyxl")
print(df.head())  
