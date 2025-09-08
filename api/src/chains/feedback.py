import os
from operator import itemgetter
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableSequence


from dotenv import load_dotenv
import sys
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))
from src.helpers.analyzer_helpers import (parse_grammar_feedback, parse_lexical_feedback,
    get_content_from_the_message)

from src.prompts_storage.prompt_constructor import create_prompt, mistakes_parser_prompt



# just mistakes objects

from src.prompts_storage.pydantic_objects import (
    GrammarMistakes,
    LexicalMistakes,
)

def build_feedback_chains(llm, part):

    coherence_feedback_chain = create_prompt(part=part, section="coherence", scope="feedback") | llm.v3

    


    coherence_feedback_chain = (
        create_prompt(part=part, section="coherence", scope="feedback")
        | llm.v3
    )

    grammar_feedback_chain = RunnableSequence(
        {
            "grammar_mistakes_unformatted": create_prompt(
                part=part, section="grammar", scope="mistakes"
            )
            | llm.r1
            | RunnableLambda(get_content_from_the_message),
            "transcript": itemgetter("transcript"),
        }
        | RunnableParallel(
            {
                "grammar_mistakes": mistakes_parser_prompt(part="grammar")
                | llm.gpt4m_0.with_structured_output(GrammarMistakes),
                "transcript": itemgetter("transcript"),
            }
        )
        | RunnableParallel(
            {
                "grammar_just_feedback": create_prompt(
                    part=part, section="grammar", scope="feedback"
                )
                | llm.v3,
                "transcript": itemgetter("transcript"),
                "grammar_mistakes": itemgetter("grammar_mistakes"),
            }
        )
        | itemgetter("grammar_just_feedback", "grammar_mistakes")
        | RunnableLambda(parse_grammar_feedback)
    )

    lexical_feedback_chain = RunnableSequence(
        {
            "lexical_mistakes_unformatted": create_prompt(
                part=part, section="lexical", scope="mistakes"
            )
            | llm.r1
            | RunnableLambda(get_content_from_the_message),
            "transcript": itemgetter("transcript"),
        }
        | RunnableParallel(
            {
                "lexical_mistakes": mistakes_parser_prompt(part="lexical")
                | llm.gpt4m_0.with_structured_output(LexicalMistakes),
                "transcript": itemgetter("transcript"),
            }
        )
        | RunnableParallel(
            {
                "lexical_just_feedback": create_prompt(
                    part=part, section="lexical", scope="feedback"
                )
                | llm.v3,
                "transcript": itemgetter("transcript"),
                "lexical_mistakes": itemgetter("lexical_mistakes"),
            }
        )
        | itemgetter("lexical_just_feedback", "lexical_mistakes")
        | RunnableLambda(parse_lexical_feedback)
    )

    feedback_chain = RunnableSequence(
        {
            "transcript": itemgetter("full_transcript"),
            "speed_of_speech": itemgetter("speed_of_speech"),
            "second_task_duration": itemgetter("second_task_duration"),
        }
        | RunnableParallel(
            {
                "coherence": coherence_feedback_chain,
                "grammar": grammar_feedback_chain,
                "lexical": lexical_feedback_chain,
            }
        )
    )
    return {'feedback_chain': feedback_chain}

