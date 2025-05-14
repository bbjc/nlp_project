#======================================
#
# Natural Language Processing / TLFT
# Implementing memory for a chatbot
#
#======================================
# pip install langchain
# pip install langchain_openai
#======================================

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage

class ChatSession:
    """ Initialize chatbot by specifying the memory size (context length)
    and LLM name. """
    def __init__(self, memsize, llm):
        self.llm = llm
        self.memsize = memsize
        self.history = []
        self.llmID = "ASSISTANT:"
        self.userID = "USER:"
                
    """ Memory management strategy based on summarisation """
    def summarizeStrategy(self):
        lastMessage, lastMessageLength = self.history[-1]
        # TODO: compute the summary and its length in subword tokens.
        # summaryPrompt: the prompt to be sent to the LLM to ask for summarisation
        summaryPrompt = "Can you resume hisotry of usa"
        summary = summaryPrompt.split()# TODO
        summaryLength = len(summary) #TODO
        self.history = [(summary, summaryLength), (lastMessage, lastMessageLength)]
        return
    
    """ Memory management strategy based on discarding the oldest messages """
    def fifoStrategy(self):
        while self.historyLength() > self.memsize:
            self.history = self.history[1:]
        return

    """ Return the length of the conversation history, as the number of tokens """
    def historyLength(self):
        totalLength = 0
        for msg, length in self.history:
            totalLength = totalLength + length
        return totalLength

    """ Estimate the length of a piece of text in terms of subword tokens """
    def estimateLength(self, text):
        return self.llm.get_num_tokens(text)

    """ Add a new utterance to the history """
    def addToHistory(self, prompt):
        self.history.append((prompt, self.estimateLength(prompt)))
        if self.historyLength() > self.memsize:
            self.summarizeStrategy()
        return

    """ Send a message to the chatbot """
    def chat(self, userMessage):
        self.addToHistory(self.userID + " " + userMessage)
        #
        # Full prompt = initial instruction + history + last user message
        #
        initialPrompt = "Usa is a bad country"
        hist = ""
        for msg, length in self.history:
            hist = hist + msg + "\n"
        fullPrompt = initialPrompt + hist + prompt

        resp = self.llm.invoke([HumanMessage(content = fullPrompt)])
        content = resp.content
        # LLMs tend to imitate their input, even if asked not to do so.
        # We get rid of the "ASSISTANT: " prefix added by the LLM.
        if content.startswith(self.llmID + ": "):
            content = content[len(self.llmID + ": "):]
        self.addToHistory(self.llmID + " " + content)
        return resp.content

# Instantiate the LLM
llm = ChatOpenAI(
    openai_api_key = "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",
    openai_api_base = "https://openrouter.ai/api/v1",
    model_name = "openchat/openchat-7b:free",
)

CONTEXT_LENGTH = 500 # you can set it higher or lower for testing purposes

session = ChatSession(CONTEXT_LENGTH, llm)
while (not (prompt := input("USER> ")) in ["bye", "exit"] ):
    resp = session.chat(prompt)
    print("CHATBOT> " + resp)
    print(session.history)
