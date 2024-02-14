from llama_index import ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
import tiktoken

from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model='ft:gpt-3.5-turbo-1106:personal::8jTDArZL', temperature=0.7)
# embed_model = OpenAIEmbedding()
# text_splitter = TokenTextSplitter(
#   separator=" ",
#   chunk_size=1024,
#   chunk_overlap=20,
#   backup_separators=["\n"],
# )
# node_parser = SimpleNodeParser.from_defaults(
#   text_splitter=text_splitter
# )
# prompt_helper = PromptHelper(
#   context_window=4096, 
#   num_output=256, 
#   chunk_overlap_ratio=0.1, 
#   chunk_size_limit=None
# )

service_context = ServiceContext.from_defaults(
  llm=llm,
#   embed_model=embed_model,
#   node_parser=node_parser,
#   prompt_helper=prompt_helper
)

documents = SimpleDirectoryReader(input_dir='body').load_data()
index = VectorStoreIndex.from_documents(
    documents, 
    service_context = service_context
    )
index.storage_context.persist()

query_engine = index.as_query_engine(service_context=service_context)
response = query_engine.query("Question: DESCRIBE IN DEPTH THE three main security properties and make sure to DESCRIBE the purpose of each one. Student's Answer: Confidentiality Mark Count: 10\n    Is this answer correct or partially? If not, provide the correct answer from the given chapters. Provide a mark out of the mark count. Feedback: Provide feedback on the accuracy and clarity of the answer if full marks were not attained. Additionally, suggest a relevant chapter or topic to study if the answer was not fully correct.")
print(response)