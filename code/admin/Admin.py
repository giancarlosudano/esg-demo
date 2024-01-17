import sys
import streamlit as st
import os
import logging
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)

st.set_page_config(page_title="Admin", page_icon=os.path.join('images','favicon.ico'), layout="wide", menu_items=None)
# mod_page_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(mod_page_style, unsafe_allow_html=True)

gre_statement_file = open(os.path.join('docs', 'gre-sgr-statement.txt'), 'r', encoding='utf-8')
statement = gre_statement_file.read()

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_BASE"), 
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    max_tokens=1000, 
    temperature=0,
    deployment_name=os.getenv("AZURE_OPENAI_MODEL"),
    model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    streaming=False
)

output_parser = StrOutputParser()

# Prova specialista EU regulation OK
prompt_eu_specialist = ChatPromptTemplate.from_messages([
    ("system", "You are a Regulatory specialist on Sustainability. You help to evaluate Company statement about ESG reporting against the 'REGULATION (EU) 2019/2088 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL of 27 November 2019'."),
    ("user", "{input}")
])

chain = prompt_eu_specialist | llm | output_parser
answer = chain.invoke({"input": "Can you summarize in a bullet point list how a ESG statement can be evaluated?"})
st.info("Question: Can you summarize in a bullet point list how a ESG statement can be evaluated?")
st.write(answer)

# Prova specialista Joint ESA
prompt_joint_esa_specialist = ChatPromptTemplate.from_messages([
    ("system", "You are a Regulatory specialist on Sustainability. You help to evaluate Company statement about ESG reporting against to the 'Joint ESA Supervisory Statement on the application of the Sustainable Finance Disclosure Regulation of 25 February 2021.'"),
    ("user", "{input}")
])

chain = prompt_joint_esa_specialist | llm | output_parser
answer = chain.invoke({"input": "Is the Join ESA supervisory statement on the application of SFDR applicable to a company like Generali Real Estate?"})
st.info("Question: Is the Join ESA supervisory statement on the application of SFDR applicable to a company like Generali Real Estate?")
st.write(answer)

chain = prompt_joint_esa_specialist | llm | output_parser
answer = chain.invoke({"input": "Can you summarize the objective of the Joint ESA supervisory statement?"})
st.info("Question: Can you summarize the objective of the Join ESA supervisory statement?")
st.write(answer)

# Prova valutazione statement da EU specialist
prompt_statement_evaluation = """Given the Generali Rel Estate ESG Statement delimited with ####

###
{statement}
###

Can you evaluate statement?"""

chain = prompt_eu_specialist | llm | output_parser
answer = chain.invoke({"input": statement.format(statement=statement)})

st.info("Evaluation of the statement (EU regulation):")
st.write(answer)

chain = prompt_joint_esa_specialist | llm | output_parser
answer = chain.invoke({"input": statement.format(statement=statement)})

st.info("Evaluation of the statement (Join ESA):")
st.write(answer)