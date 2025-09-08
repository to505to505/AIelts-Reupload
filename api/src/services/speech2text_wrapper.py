from abc import ABC, abstractmethod
from io import BytesIO
import httpx
import os
import asyncio
from openai import OpenAI
from src.models import  TranscriptOutput
from pydantic import BaseModel, Field





class Speech2TextModel(ABC):
    @abstractmethod

    async def get_transcript(self, file: BytesIO): ...




class IELTSWhisper(Speech2TextModel):

    ''' Whisper'''

    def __init__(self, response_format = 'verbose_json', prompt = '', temperature = 0.5, timestamp_granularities =["word"] , language = 'en'):

        self._openai =  OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        http_client=(
            httpx.Client(timeout=60 * 7, proxy=os.getenv("PROXY"))
            if os.getenv("PROXY")
            else httpx.Client(timeout=60 * 7)
        ))

        self._response_format = response_format
        self._vibe_prompt = prompt
        self._temprature = temperature
        self._timestamp_granularities = timestamp_granularities
        self._language = language

    
    def _create_transcription(self, file):
        return self._openai.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format=self._response_format,
            prompt=self._vibe_prompt,
            temperature=self._temprature,
            timestamp_granularities=self._timestamp_granularities,
            language=self._language,
        )


    async def get_transcript(self, file: BytesIO,):
        transcription = await asyncio.to_thread(
            self._create_transcription,
            file
        )
        return transcription
