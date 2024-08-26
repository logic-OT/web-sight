from langchain.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceEmbeddings


from huggingface_hub import login
token = os.getenv("HUGGING_FACE_HUB_TOKEN")
login(token)

callbacks = [StreamingStdOutCallbackHandler()]
embedder = HuggingFaceEmbeddings(model_name = 'all-MiniLM-L6-v2')

model = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=token,
    verbose=True,
    temperature=0.25,
    top_p=0.9,
    repetition_penalty=1.2
)
system_prompt = PromptTemplate(
    template="System: Your name is Web-sight. You were designed to extract content from a websites. If a user's instruction does contain an instruction that requires you to visit a website, answer them but remind them that you are a website analyser and you would like them to add a link or url to their query so you can look at the website. \n\n Human: {user_query} \n\n AI: ",
    input_variables=['user_query']
)

prompt = PromptTemplate(
    template= "System: You are an expert link checker. Your task is to determine if there is any link, URL, or webpage (such as those containing 'http', 'https', 'www', or '.com', '.org', etc.) in the user's query. If you find any link or URL, answer 'yes'. If you find none, answer 'no'. Do not provide any explanation, just answer 'yes' or 'no'. \n\n Human: {user_query} \n\n Is there a link to a website in the above text? Answer strictly 'yes' or 'no': \n\n AI:",
    input_variables=['user_query']
)
prompt_1 = PromptTemplate(
    template= "You are a link extractor AI. Your job is to only look for links in from user messages. Given a message from a user, extract all the links in the query in the format: ['link','link'] ALWAYS respond with only a link. \n\n Human: {user_query} \n Please, extract all the links in the above message. Respond with the links in the right format \n\n AI:",
    input_variables=['user_query']
    )
prompt_2= PromptTemplate(
    template= "You are an instruction extractor AI. Given an instruction from a user, Summarize what the user is asking for. Don't give any further explanation \n\n Human: {user_query} \n\n AI:",
    input_variables=['user_query']
    )
prompt_3= PromptTemplate(
    template= "You are an instruction validator AI. Your job is to check whether the user's query requires as to know the content from a websit. Answer strictly yes or no in one word \n\n Human: {user_query} \n Does the above message require us to know the content of the site?? Answer strictly yes or no in one word \n\n AI:",
    input_variables=['user_query']
    )

final_prompt = PromptTemplate(
    template="System: This is context collected from a website. Summarize the given context as an answer to the question provided. Be as detailed as you wish. When refering to the context, always use 'website' or 'webpage'. For example, according to the website, \n\n Context: {context} \n\n Question: {question} \n\n Answer:",
    input_variables=['context','question'])

system_prompt_chain = LLMChain(llm=model, prompt=system_prompt)
chain = LLMChain(llm=model, prompt=prompt)
chain1 = LLMChain(llm=model, prompt=prompt_1)
chain2 = LLMChain(llm=model, prompt=prompt_2)
chain3 = LLMChain(llm=model, prompt=prompt_3)
final_chain = LLMChain(llm=model, prompt=final_prompt)