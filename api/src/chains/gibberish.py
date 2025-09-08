
import os
from langchain_core.runnables import RunnableLambda
import pandas as pd
from dotenv import load_dotenv
import sys
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))



from src.services.exceptions import NotRelatedToIELTS
from src.prompts_storage.prompt_constructor import create_prompt




def check_for_gibberish(gibberish_str):
    if os.getenv("PROD") == "true" and gibberish_str.content == "no":
        raise NotRelatedToIELTS("The input is not related to IELTS")


def build_gibberish_chain(llm, part ):
    ''' Building a chain for gibberish detection '''

    gibberish_chain = create_prompt(part=part, scope="gibberish") | llm.gpt4m_02 | RunnableLambda(check_for_gibberish)
    
    return {"gibberish_chain": gibberish_chain}

