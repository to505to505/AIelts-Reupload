import os
import asyncio
import logging
import json
import httpx


from dotenv import load_dotenv
import sys
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))

from src.services.llm_wrapper import LLMWrapper
from src.helpers.analyzer_helpers import concat_parts
from src.models import (
    Answer, Criterion, Feedback, Grammar as GrammarModel, GrammarMistake,
    Lexical as LexicalModel, Coherence as CoherenceModel, LexicalMistake
)



from src.chains.grades import build_grades_chains
from src.chains.feedback import build_feedback_chains
from src.chains.gibberish import build_gibberish_chain

from src.data_setup.IELTSDataset import IELTSDataset

from src.services.exceptions import NotRelatedToIELTS

from src.helpers.analyzer_helpers import add_indices_mistakes

### Setting up logger 
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


### Data for prediction 
ielts_dataset = IELTSDataset(name = 'BetaBase')
df = ielts_dataset.df



def process_results(grades, feedback, full_transcript, speed_of_speech, part ):

    ''' Processing results to return to database in a certain format '''
    if part == 0:
        # Извлечение оценок
        grammar = max(1, grades.get("Grammar"))
        coherence = max(1, grades.get("Coherence"))
        lexical = max(1, grades.get("Lexical"))

        # Проверка на нерелевантность для IELTS
        if (grammar <= 2 or coherence <= 2 or lexical <= 2) and os.getenv("PROD") == "true":
            raise NotRelatedToIELTS("The input is not related to IELTS speaking exam. The grades are 0 for all 3 categories.")

    # Сортировка ошибок
    indencies_grammar, indencies_lexical = add_indices_mistakes(feedback, full_transcript)

    # Формирование объектов ошибок
    MistakesGrammarObject = [
        GrammarMistake(wrong=wrong, correct=correct, type=mistake_type)
        for wrong, correct, mistake_type in zip(
            feedback["grammar"].ActualVersions,
            feedback["grammar"].CorrectedVersions,
            feedback["grammar"].TypeOfMistake,
        )
    ]
    MistakesLexicalObject = [
        LexicalMistake(wrong=original, correct=rephrased)
        for original, rephrased in zip(
            feedback["lexical"].OriginalSentences,
            feedback["lexical"].RephrasedSentences,
        )
    ]

    sortedmistakesGrammarObject = sorted(zip(MistakesGrammarObject, indencies_grammar), key=lambda x: x[1])
    sortedmistakesLexicalObject = sorted(zip(MistakesLexicalObject, indencies_lexical), key=lambda x: x[1])

    # Создание итогового объекта Feedback
    feedback_result = Feedback(
        grammar=GrammarModel(
            criterion=Criterion(
                score=float(grammar) if part==0 else 100,
                text=feedback["grammar"].CommentaryGrammar,
            ),
            mistakes=[x[0] for x in sortedmistakesGrammarObject],
        ),
        lexical=LexicalModel(
            criterion=Criterion(
                score=float(lexical) if part==0 else 100,
                text=feedback["lexical"].CommentaryLexical,
            ),
            mistakes=[x[0] for x in sortedmistakesLexicalObject],
        ),
        coherence=CoherenceModel(
            criterion=Criterion(
                score=float(coherence) if part==0 else 100,
                text=feedback["coherence"].content,
            ),
            speed=speed_of_speech,
        ),
    )
    return feedback_result




async def retry_chain(chain, input_data, chain_name, client, async_client, part, max_attempts=3):
    '''
    Функция для повторных попыток выполнения цепочек в случае ошибок.

    '''

    errors = []
    chain = chain 
    
    for attempt in range(max_attempts):
        try:
            result = await chain.ainvoke(input_data)
            return result
        
        except json.JSONDecodeError as e:
            error_message = f"Ошибка в {chain_name} (попытка {attempt + 1}): {str(e)}"
            logger.warning(error_message)
            errors.append(error_message)
            if attempt < max_attempts - 1:
                llm = LLMWrapper(client, async_client, highload=True)
                if chain_name == "feedback_chain":
                    chain = build_feedback_chains(llm, part)['feedback_chain']
                else:
                    chain = build_grades_chains(llm, part)['grade_chain']
            else:
                logger.error(f"Все попытки для {chain_name} провалились.  Still high load even for v3! Ошибки: {errors}")
                return {
                    "error": {
                        "message": f"Все попытки для {chain_name} провалились. Still high load even for v3! JSONDecodeError: {errors}",
                        "code": 9990
                    }
                }

        except NotRelatedToIELTS as e:
            # Немедленно прерываем выполнение и возвращаем ошибку
            logger.error(f"NotRelatedToIELTS в {chain_name}: {str(e)}")
            return {"error": {"code": 1000, "message": str(e)}}
        except Exception as e:
            # Обрабатываем любые другие исключения
            if hasattr(e, 'status_code') and e.status_code in [500, 503]:
                return {
                    "error": {
                        "message": f"{str(e)}",
                        "code": e.status_code
                    }
                }
            error_message = f"Ошибка в {chain_name} (попытка {attempt + 1}): {str(e)}"
            logger.warning(error_message)
            errors.append(error_message)
            if attempt == max_attempts - 1:
                logger.error(f"Все попытки для {chain_name} провалились. Ошибки: {errors}")
                for error in errors:
                    if error != error_message:
                        return {
                            "error": {
                                "message": f"Все попытки для {chain_name} провалились с разными ошибками. Ошибки: {errors}",
                                "code": 9998
                            }
                        }
                return {
                    "error": {
                        "message": f"Все попытки для {chain_name} провалились с ошибкой: {error_message}",
                        "code": 9999
                    }
                }

   


async def analyze(answers: list[Answer], speed_of_speech: float, part: int, attempt_id: str) -> dict | Feedback:

    ''' Central function called from main.py'''


    try:
        
        ### Setting up some stuff 

        # Setting up http clients
        client = httpx.Client(timeout=60 * 15, proxy=os.getenv("PROXY")) if os.getenv("PROXY") else httpx.Client(timeout=60 * 15)
        async_client = httpx.AsyncClient(timeout=60 * 15, proxy=os.getenv("PROXY")) if os.getenv("PROXY") else httpx.AsyncClient(timeout=60 * 15)

        # setting up llm models
        llm = LLMWrapper(client, async_client)

        # building chains in advance
        grade_chain = None
        feedback_chain = build_feedback_chains(llm, part)['feedback_chain']
        gibberish_chain = build_gibberish_chain(llm, part)['gibberish_chain']

        # creating transcript  
        if part == 0 : 
            transcript = concat_parts(answers[0].text, answers[1].text, answers[2].text)
            grade_chain = build_grades_chains(llm, df)
        else: 
            transcript = answers[0].text


        ### Starting chains 

        # gibberish check 
        await gibberish_chain.ainvoke({"transcript": transcript })


        # Input data for feedback chain
        feedback_input = {
            "full_transcript": transcript,
            "speed_of_speech": speed_of_speech,
            "second_task_duration": int(answers[0].duration_seconds) if part==2 else int(answers[0].duration_seconds) if part==0 else 0,
        }
        # Running feedback chain
        feedback_task = asyncio.create_task(retry_chain(feedback_chain, feedback_input, "feedback_chain", client, async_client, part))

        grades = None
        # Starting chains 
        if part == 0:
            grade_input = {
                "full_transcript": transcript,
                "speed_of_speech": speed_of_speech,
                "second_task_duration": int(answers[1].duration_seconds),
                **grade_chain['dop_infa'],
            }
            grades_task = asyncio.create_task(retry_chain(grade_chain['grade_chain'], grade_input, "grade_chain", client, async_client, part))
            grades, feedback = await asyncio.gather(grades_task, feedback_task)

        else: 
            feedback = await feedback_task

        
        # Checking results for errors
        if (isinstance(grades, dict) and 'error' in grades): 
            return grades
        if (isinstance(feedback, dict) and 'error' in feedback):
            return feedback
      
        
        # Processing results
        
        feedback_result = process_results(grades, feedback, transcript, speed_of_speech, part)
        return feedback_result

    except NotRelatedToIELTS as e:
        error_result = e.to_dict()
        logger.error(f"Ошибка NotRelatedToIELTS: {error_result}")
        return error_result
    
    except Exception as e:
        error_result = {
            "error": {
                "code": 9997,
                "message": f"Неожиданная ошибка вне выполнения цепочек : {str(e)}"
            }
        }
        logger.error(f"Неизвестная ошибка: {error_result}")
        return error_result