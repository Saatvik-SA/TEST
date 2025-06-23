
 
# Path to your .sqlite file
database_path = 'C:\\Users\\saatv\\Downloads\\olist.sqlite'
conn_str = f'sqlite:///{database_path}'
  
# Create a connection string

from langchain_community.utilities.sql_database import SQLDatabase  # Import the SQLDatabase class

db = SQLDatabase.from_uri(conn_str)

import os
from getpass import getpass

# Set an environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBA9jfrJInryKsO3vL927hOekpFadv8Bi8'

# Retrieve the environment variable
value = os.getenv('GOOGLE_API_KEY')
print(f'GOOGLE_API_KEY: {value}')

geminiai_key = os.getenv('GOOGLE_API_KEY')

if(geminiai_key == None):
  geminiai_key = getpass('Provide your GeminiAI API key: ')
if(not geminiai_key):
  raise ValueError("GeminiAI API key not provided.")
print('GemininAI API key is set')

import google.generativeai as GenAI
GenAI.configure(api_key=geminiai_key)
 
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm =  ChatGoogleGenerativeAI(model="gemini-pro")
agent = create_sql_agent(llm, db=db, agent_type="zero-shot-react-description", verbose=True)

prefix = "You are an expert in data analysis. As an expert you must iterate through multiple sheets of the dataset . Answer the following question: "
suffix = " Make sure your response is clear and concise."

from langchain_community.callbacks import get_openai_callback


query = input("Enter your query: ")
full_query = f"{prefix}{query}{suffix}"

with get_openai_callback() as cb:
  response = agent.run(full_query)
  print(response)
  Total_tokens = cb.total_tokens
  Prompt_tokens = cb.prompt_tokens
  Completion_tokens = cb.completion_tokens
  Total_cost = cb.total_cost
  print(f"Total Tokens: {Total_tokens}")
  print(f"Prompt Tokens: {Prompt_tokens}")
  print(f"Completion Tokens: {Completion_tokens}")
  print(f"Total Cost (USD): ${Total_cost}")