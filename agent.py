import re, requests,ast
from chains_and_vars import *
from scraper import extract_info
from RAG import RAG


def Model(user_query):
    is_link = PromptTemplate(
    input_variables=['query'],
    template = prompt.format(user_query="{query}")
    )
    try:
      link_chain = LLMChain(llm=model, prompt=is_link)
      answer = link_chain.run(user_query)
      if 'yes' in answer.lower():
        if_open = chain3.run(user_query)
        print("if_open: ",if_open)
        if 'yes' in if_open.lower():
          find_links = chain1.run(user_query)
          print(find_links)
          links = re.findall(r'\[.*?\]',find_links)[0]
          links = ast.literal_eval(links)
          content = extract_info(links[0])
          instruction = chain2.run(user_query)
          response = RAG(content,instruction)
          return response
        else:
          return system_prompt_chain.run(user_query, callbacks=callbacks)
      else:
        return system_prompt_chain.run(user_query, callbacks=callbacks)
    except:
      return "There was a problem responding to your query. Please try again later!"
