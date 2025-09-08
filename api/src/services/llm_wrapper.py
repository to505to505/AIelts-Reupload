import os

from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek


class LLMWrapper:

    ''' Class for setting up all available models.'''
    
    def __init__(self, http_client = None, http_async_client = None, test=False, highload=False):

        ''' If test == true, then we are testing this shit offline '''
        if not test:
            self.http_client = http_client
            self.http_async_client = http_async_client

            self.gpt3_001 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.01,
                model="gpt-3.5-turbo-0125",
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )
            self.gpt4m_02 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.2,
                model="gpt-4o-mini",
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )

            self.gpt4m_0 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0,
                model="gpt-4o-mini",
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )


            self.gpt4m_08 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.8,
                model="gpt-4o-mini",
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )
            self.gpt4o = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.2,
                model="gpt-4o",
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )

            self.v3 = ChatDeepSeek(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                model="deepseek-chat",
                temperature=1,
                timeout=None,
                max_retries=3,
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )
            if highload:
                self.r1 = ChatDeepSeek(
                    api_key=os.getenv("DEEPSEEK_API_KEY"),
                    model="deepseek-chat",
                    temperature=0.2,
                    timeout=None,
                    max_retries=3,
                    max_tokens=2000,
                    http_client=self.http_client,
                    http_async_client=self.http_async_client,
                )
            else:
                self.r1 = ChatDeepSeek(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                model="deepseek-reasoner",
                temperature=0.5,
                timeout=None,
                max_retries=3,
                max_tokens=2000,
                http_client=self.http_client,
                http_async_client=self.http_async_client,
            )

        
        else:
            self.gpt3_001 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.01,
                model="gpt-3.5-turbo-0125"
            )
            self.gpt4m_02 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.2,
                model="gpt-4o-mini"
            )
            self.gpt4m_0 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0,
                model="gpt-4o-mini"
            )
            self.gpt4m_08 = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.8,
                model="gpt-4o-mini"
            )
            self.gpt4o = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.2,
                model="gpt-4o"
            )
            self.v3 = ChatDeepSeek(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                model="deepseek-chat",
                temperature=0.1,
                timeout=None,
                max_retries=5,
              
            )

            self.r1 = ChatDeepSeek(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                model="deepseek-reasoner",
                temperature=0.5,
                timeout=None,
                max_retries=5,
                max_tokens=2000,
              
            )
