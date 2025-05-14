# pip install langchain
# pip install langgraph
# pip install langchain_openai

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
  openai_api_key="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",
  openai_api_base="https://openrouter.ai/api/v1",
  model_name="openchat/openchat-7b:free",
)
resp = llm.invoke([HumanMessage(content="Hi how are you?")])
print(resp)
print(resp.content)

