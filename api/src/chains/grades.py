import os
from operator import itemgetter
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableSequence

import pandas as pd
from dotenv import load_dotenv
import sys
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))


from src.helpers.data_helpers import  get_string_from_dataset, get_examples_csv_by_ids


from src.prompts_storage.prompts import (
    overall_ielts_instructions, grade_by_grade_instructions_str, prompt_base,
    prompt_select_examples, prompt_adjust_grades_by_example
)
from src.prompts_storage.pydantic_objects import Grades, SelectedExamples


def finalize_grades(all_args: tuple) -> dict:
    ''' Averaging grades from different models in our chain into final grades'''
    import numpy as np
    grades_refined, grades_1, grades_2 = all_args
    final_list = []
    grades_refined = np.array([grades_refined.Coherence, grades_refined.Grammar, grades_refined.Lexical])
    grades_1 = np.array([grades_1.Coherence, grades_1.Grammar, grades_1.Lexical])
    grades_2 = np.array([grades_2.Coherence, grades_2.Grammar, grades_2.Lexical])

    if np.mean(grades_1) <= 2:
        final_list = [0, 0, 0]
    elif np.mean(grades_2) >= 7.3:
        if np.mean(grades_1) >= 7:
            final_list = list(map(lambda x: round(x * 2) / 2, (grades_refined + grades_1 + grades_2 + np.array([1.5, 2, 1.5])) / 3))
        else:
            final_list = list(map(lambda x: round(x * 2) / 2, (grades_refined + grades_1 + np.array([0.5, 1, 0.5])) / 2))
    elif np.mean(grades_2) <= 5:
        final_list = list(map(lambda x: round(x * 2) / 2, (4 * grades_refined + grades_1 + grades_2) / 6))
    else:
        final_list = list(map(lambda x: round(x * 2) / 2, grades_refined))

    return {"Coherence": final_list[0], "Grammar": final_list[1], "Lexical": final_list[2]}




def build_grades_chains(llm, df):
    ''' Building chains for the analyzer '''
    # Цепочка для оценок
    grade_chain = RunnableSequence(
        RunnableParallel(
            {
                "grades_1": prompt_base | llm.gpt4m_08.with_structured_output(Grades),
                "grades_2": prompt_base | llm.gpt3_001.with_structured_output(Grades),
                "full_transcript": itemgetter("full_transcript"),
                "speed_of_speech": itemgetter("speed_of_speech"),
                "csv_examples_data": itemgetter("csv_examples_data"),
            }
        )
        | RunnableParallel(
            {
                "selected_examples_ids": prompt_select_examples | llm.gpt4o.with_structured_output(SelectedExamples),
                "grades_1": itemgetter("grades_1"),
                "grades_2": itemgetter("grades_2"),
                "full_transcript": itemgetter("full_transcript"),
                "speed_of_speech": itemgetter("speed_of_speech"),
            }
        )
        | RunnableParallel(
            {
                "selected_examples_csv": itemgetter("selected_examples_ids") | RunnableLambda(lambda ids: get_examples_csv_by_ids(df, ids)),
                "grades_1": itemgetter("grades_1"),
                "grades_2": itemgetter("grades_2"),
                "full_transcript": itemgetter("full_transcript"),
                "speed_of_speech": itemgetter("speed_of_speech"),
            }
        )
        | RunnableParallel(
            {
                "grades_refined": prompt_adjust_grades_by_example | llm.gpt4o.with_structured_output(Grades),
                "grades_1": itemgetter("grades_1"),
                "grades_2": itemgetter("grades_2"),
            }
        )
        | itemgetter("grades_refined", "grades_1", "grades_2")
        | RunnableLambda(finalize_grades)
    )

    


    
    
    dop_infa = {
        "csv_examples_data": get_string_from_dataset(df),
        "overall_ielts_instructions": overall_ielts_instructions,  # Предполагается, что это определено где-то выше
        "grade_by_grade_instructions_str": grade_by_grade_instructions_str,  # Аналогично
    }


    return {
        "grade_chain": grade_chain,
        "dop_infa" : dop_infa
    }
