from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
def create_title(message):
    prompt_template = PromptTemplate(
        input_variables=["input_text"],
        template="Return short chat title from the following input: '{input_text}' Return only the title and nothing else."
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
    chain = prompt_template | llm
    response = chain.invoke(message)
    return response.content