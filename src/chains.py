from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
import streamlit as st
from src.schema import LegalResponse
from src.prompts import legal_prompt
from src.rag import get_retriever

## load_dotenv() use in local
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
parser = PydanticOutputParser(
    pydantic_object=LegalResponse
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    #''for deployment'''
    api_key=GROQ_API_KEY 
)

retriever = get_retriever()


def ask_legal_assistant(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    chain = (
        legal_prompt.partial(
            format_instructions=
            parser.get_format_instructions()
        )
        | llm|parser
    )

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response