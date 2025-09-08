from langsmith.schemas import Run, Example
from langsmith.evaluation import evaluate

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder


from langchain_openai import ChatOpenAI



from pydantic import BaseModel, Field


import json
from typing import Tuple, List
import os



os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["LANGSMITH_PROJECT"] ="ielts-test"


# BASIC STATIC STUFF WE NEED FOR EVALUATING 

# basic IELTs grading criteria context
all_instructions  = "Fluency and coherence: for grade 9: Fluent with only very occasional repetition or self-correction. Any hesitation is content-related, not to find words or grammar. Fully coherent and appropriately extended topic development.; \nfor grade 8: Fluent with occasional repetition or self-correction. Hesitations are mostly content-related. Coherent and relevant topic development.; \nfor grade 7: Able to keep going and readily produce long turns without noticeable effort. Some hesitation, repetition, and/or self-correction may occur, often mid-sentence, indicating problems with accessing appropriate language. However, these do not affect coherence.; \nfor grade 6: Able to keep going and demonstrates a willingness to produce long turns. Coherence may be lost at times due to hesitation, repetition, and/or self-correction.; \nfor grade 5: Usually able to keep going, but relies on repetition and self-correction to do so and/or on slow speech. Hesitations are often associated with mid-sentence searches for basic lexis and grammar.; \nfor grade 4: Unable to keep going without noticeable pauses. Speech may be slow with frequent repetition. Often self-corrects. Can link simple sentences but often with repetitious use of connectives. Some breakdowns in coherence.; \nfor grade 3: Frequent, sometimes long, pauses occur while candidate searches for words. Limited ability to link simple sentences and go beyond simple responses to questions. Frequently unable to convey basic message.; \nfor grade 2: Lengthy pauses before nearly every word. Isolated words may be recognisable but speech is of virtually no communicative significance.; \nfor grade 1: Essentially none. Speech is totally incoherent. No resource bar a few isolated words. No communication possible.\n\nLexical resource: for grade 9: Total flexibility and precise use in all contexts, with idiomatic language. Vocabulary is situationally appropriate.; \nfor grade 8: Wide resource, flexible use for all topics. Skilful use of less common items with some inaccuracies.; \nfor grade 7: Resource flexibly used to discuss a variety of topics. Some ability to use less common and idiomatic items and an awareness of style and collocation is evident, though inappropriacies occur. Effective use of paraphrase as required.; \nfor grade 6: Resource sufficient to discuss topics at length. Vocabulary use may be inappropriate but meaning is clear. Generally able to paraphrase successfully.; \nfor grade 5: Resource sufficient to discuss familiar and unfamiliar topics but with limited flexibility. Attempts paraphrase but not always with success.; \nfor grade 4: Resource sufficient for familiar topics but only basic meaning can be conveyed on unfamiliar topics. Frequent inappropriacies and errors in word choice. Rarely attempts paraphrase.; \nfor grade 3: Resource limited to simple vocabulary used primarily to convey personal information. Vocabulary inadequate for unfamiliar topics.; \nfor grade 2: Very limited resource. Utterances consist of isolated words or memorised utterances. Little communication possible without the support of mime or gesture.; \nfor grade 1: No rateable language unless memorised.\n\nGrammatical range and accuracy: for grade 9: Structures are precise and accurate with native-like 'mistakes'.; \nfor grade 8: Wide range of structures, flexibly used. Most sentences are error-free with occasional basic errors.; \nfor grade 7: A range of structures flexibly used. Error-free sentences are frequent. Both simple and complex sentences are used effectively despite some errors. A few basic errors persist.; \nfor grade 6: Produces a mix of short and complex sentence forms and a variety of structures with limited flexibility. Though errors frequently occur in complex structures, these rarely impede communication.; \nfor grade 5: Basic sentence forms are fairly well controlled for accuracy. Complex structures are attempted but limited in range, often containing errors.; \nfor grade 4: Can produce basic sentence forms and some short utterances are error-free. Subordinate clauses are rare, and overall, turns are short, structures are repetitive, and errors are frequent.; \nfor grade 3: Basic sentence forms are attempted but grammatical errors are numerous except in apparently memorised utterances.; \nfor grade 2: No evidence of basic sentence forms.; \nfor grade 1: Can produce occasional individual words and phonemes that are recognisable, but no overall meaning is conveyed."


# class for evaluating grades
class Grades(BaseModel):
    ''' Just putting grades float grades for 3 IETLS criteria. NEVER leave these fields empty and NEVER put null or none values. '''
    Arguments: str = Field(description = "Give sufficient and concise argumentation for choosen grades. ")
    Coherence: float = Field( description= "Grade for Fluency and Coherence category. Just the grade! If you can't put any grade, just put 0. Always put something here. NEVER leave this field as None or null. ")
    Lexical: float = Field( description = "Grade for Lexical Resource category. Just the grade! If you can't put any grade, just put 0. Always put something here. NEVER leave this field as None or null. ")
    Grammar: float = Field( description = "Grade for Grammatical range and accuracy category. Just the grade! If you can't put any grade, just put 0. Alwaya put something here. NEVER leave this field as None or null.")
    

# output parser
grades_parser = JsonOutputParser(pydantic_object=Grades)


# AUXILIARY FUNCTIONS

def process_output(run: Run, example: Example) -> Tuple[Grades, List[float]]:

    ''' Processing output in order to get real and predicted grades in a convenient format'''
    
    output = run.outputs
    real = []
    real.append(example.outputs['Coherence'])
    real.append(example.outputs['Lexical'])
    real.append(example.outputs['Grammar'])

    if(output.get("Coherence") == None ):
        output['Coherence'] = 0 
    if(output.get("Lexical") == None ):
        output['Lexical'] = 0 
    if(output.get("Grammar") == None ):
        output['Grammar'] = 0 

   
    return output, real


# BLOCK WITH EVALUATORS 

def diff(run: Run, example: Example) -> dict:

    ''''Total absolute difference between real grades and predicted'''

    
    output, real = process_output(run, example)

    diff = abs(output.get("Coherence") - real[0])
    diff += abs(output.get("Lexical") - real[1])
    diff += abs(output.get("Grammar") - real[2])

    
    return {'key': 'diff', 'score': diff}


def deviation(run: Run, example: Example) -> dict:

    ''' Deviation more than 1 point count '''

    output, real = process_output(run, example)

    deviation_more_than_1 = sum(1 for a,b in zip([output.get("Coherence"), output.get("Lexical") , output.get("Grammar") ], real) if abs(a-b)>1  )
    
    return {'key': 'deviation_more_than_1', 'score': deviation_more_than_1} 


def correct_percentage(run: Run, example: Example) -> dict:
    output, real = process_output(run, example)

    match_count = sum(1 for a, b in zip([output.get("Coherence") , output.get("Lexical") , output.get("Grammar") ], real) if a == b)
    correct_percentage = match_count/len(real)
    return {'key': 'correct_percentage', 'score': correct_percentage}


# BLOCK WITH SUMMARY EVALUATORS

def diff_total(runs: List[Run], examples: List[Example]) -> dict:
    diff_total = 0
    
    for run, example in zip(runs, examples):
        diff_dict = diff(run, example)
        diff_total += diff_dict.get('score')
    return {'key': 'diff_total', 'score': diff_total}

def deviation_total(runs: List[Run], examples: List[Example]) -> dict:
    
    deviation_total = 0 
    for run, example in zip(runs, examples):
        deviation_dict = deviation(run, example)
        deviation_total += deviation_dict.get('score')
    return {'key': 'deviation_total', 'score': deviation_total}


def correct_percentage_total(runs: List[Run], examples: List[Example]) -> dict:
    
    correct_percentage_total = 0 
    for i, (run, example) in enumerate(zip(runs, examples)):
        correct_percentage_dict = correct_percentage(run, example)
        correct_percentage_total += correct_percentage_dict.get('score')
    return {'key': 'correct_percentage_total', 'score': correct_percentage_total/+(i+1)}



# ACTUAL FUNCTION FOR GENERATING OUTPUT 

def answer_grades(inputs: dict, chain: RunnableSequence, dop_infa: dict) -> dict:
   
    global grades_parser


    ### MIDDLEWARE

    
    input_data = {"full_transcript": inputs['full_transcript'], "speed_of_speech": inputs['speed_of_speech'], "second_task": inputs['second_task'], 'second_task_duration': inputs['second_task_duration'] } | dop_infa
    


    
    output = chain.invoke(input_data)
    

    # Response in output dict
    
    return output



 



evaluators = [diff, deviation, correct_percentage]
summary_evaluators = [diff_total, deviation_total, correct_percentage_total]
# dataset_name = 'Base_7'




def add_chain(chain, dop_infa):
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs['chain'] =chain
            kwargs['dop_infa'] = dop_infa
            return func(*args, **kwargs)
        return wrapper
    return decorator

# FINAL FUNCTION
def final_evaluation(chain: RunnableSequence, experiment_prefix: str, dataset: str, dop_infa: dict):
    
        custom_answer_grades = add_chain(chain = chain, dop_infa = dop_infa)(answer_grades)
        experiment_results = evaluate(
            custom_answer_grades,
            data=dataset,
            evaluators=evaluators,
            summary_evaluators=summary_evaluators,
            experiment_prefix=experiment_prefix,
            
            metadata={
                
            },
        )
   