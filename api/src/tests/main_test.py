import pytest
import sys
import os
from dotenv import load_dotenv

# Load environment variables and set up sys.path
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))

from src.services.transcriber import transcribe_audio
from src.models import Feedback  

def check_feedback(result):
    """
    Helper function to validate the result from transcribe_audio.
    - Fails if an error dictionary is returned, displaying the error message.
    - Ensures the result is a Feedback object with non-empty commentary texts.
    """

    if isinstance(result, dict) and "error" in result:
        pytest.fail(f"Error occurred: {result['error']['message']}")
    assert isinstance(result, Feedback), "Expected a Feedback object, got something else"
    assert len(result.grammar.criterion.text.strip()) >=10, "Grammar commentary is empty"
    assert len(result.lexical.criterion.text.strip()) >=10, "Lexical commentary is empty"
    assert len(result.coherence.criterion.text.strip()) >=10, "Coherence commentary is empty"
    assert result.grammar.criterion.score >= 0, "Grammar score is negative"
    assert result.lexical.criterion.score >= 0, "Lexical score is negative"
    assert result.coherence.criterion.score >= 0, "Coherence score is negative"


@pytest.mark.asyncio
async def test_transcribe_audio_full():
    """Test the full transcription scenario."""
    await transcribe_audio('l791g2kvil5hm97', 'br8tdd767kvy83f', test=True)
    await transcribe_audio('sj0nb305blrt97u', 'br8tdd767kvy83f', test=True)
    result = await transcribe_audio('v5v997rd6p8400u', 'br8tdd767kvy83f', test=True)

    check_feedback(result)

@pytest.mark.asyncio
async def test_transcribe_audio_part1():
    """Test the part1 transcription scenario."""
    result = await transcribe_audio('o9x5gv0p2ck2718', 'qqd6at29kiz0199', test=True)
    
    check_feedback(result)

@pytest.mark.asyncio
async def test_transcribe_audio_part2():
    """Test the part2 transcription scenario."""
    result = await transcribe_audio('jlto7y9d619fpv9', 'x4c102fwkt6li70', test=True)
   
    check_feedback(result)

@pytest.mark.asyncio
async def test_transcribe_audio_part3():
    """Test the part3 transcription scenario."""
    result = await transcribe_audio('q158v0286g7dxdr', '5j3w78teg6meb48', test=True)
    
    check_feedback(result)