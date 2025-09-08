from langchain_core.output_parsers import JsonOutputParser
from json import JSONDecodeError
from typing import  Any

import re

from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation
from langchain_core.utils.json import (

    parse_json_markdown,

)

class JsonOutputParserReasoner(JsonOutputParser):
    ''' 
    Rewritten JsonOutputParser to parse the output of the NOVITA AI  Reasoner deepseek model (we delete his thoughs)



    !!! DEPRECATED FOR NOW !!!

    !!! NOT IN USE !!!!



    '''

    def parse_result(self, result: list[Generation], *, partial: bool = False) -> Any:
        """Parse the result of an LLM call to a JSON object.

        Args:
            result: The result of the LLM call.
            partial: Whether to parse partial JSON objects.
                If True, the output will be a JSON object containing
                all the keys that have been returned so far.
                If False, the output will be the full JSON object.
                Default is False.

        Returns:
            The parsed JSON object.

        Raises:
            OutputParserException: If the output is not valid JSON.
        """
        text = result[0].text
        text = text.strip()
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        if partial:
            try:
                return parse_json_markdown(text)
            except JSONDecodeError:
                return None
        else:
            try:
                return parse_json_markdown(text)
            except JSONDecodeError as e:
                msg = f"Invalid json output: {text}"
                raise OutputParserException(msg, llm_output=text) from e

