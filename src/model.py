from llama_index.core import Settings
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.prompts import RichPromptTemplate

from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

from llama_index.tools.google import GmailToolSpec
from tools import make_tools

from credentials import google_api_key
from embedding import EmbeddingManager
from contract_storage import ContractStorage


def make_agent():
    llm = GoogleGenAI(
        model="models/gemini-2.5-flash",
        api_key = google_api_key
    )

    # Settings
    Settings.embed_model = GoogleGenAIEmbedding(
        model_name="text-embedding-004",
        api_key = google_api_key
    )

    Settings.chunk_size = 800
    Settings.context_window = 160000

    # Embedding & Others
    embeddingManager = EmbeddingManager(initial_filepath = "data/initial_data")
    contractStorage = ContractStorage()

    # Tools
    my_tools = make_tools(llm, embeddingManager, contractStorage)
    tool_spec = GmailToolSpec()
    gmail_tools = [tool_spec.create_draft, tool_spec.send_draft,
                    tool_spec.load_data, tool_spec.search_messages]
    
    agent = FunctionAgent(llm=llm, tools = my_tools + gmail_tools, max_iterations=3)

    return agent

def make_memory():
    chat_store = SimpleChatStore()

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=24000,
        chat_store=chat_store,
        chat_store_key="user1",
    )

    return chat_memory

def make_prompt_template(context_str, filepath = "resources/prompts/prompt_template.txt"):
    with open(filepath, 'r') as file:
        qa_template = RichPromptTemplate(file.read())
        prompt = qa_template.format_messages(context_str=context_str)
        return prompt