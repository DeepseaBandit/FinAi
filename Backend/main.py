import pandas as pd
import requests
import openpyxl

from langchain_together import Together

df = pd.read_csv("AdaniGreen.csv")
print(df.head())  
