from io import StringIO
import os


import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))

from gen.src.services.analyzer_single_part import AnalyzerSingle

from langchain.smith.evaluation import run_on_dataset
from langsmith import evaluate, Client
from langchain_core.runnables import RunnableLambda




# Initializing grades_chain


def create_set_lambda(part):

    def set_second_task_duration(input_dict):

        transcript = input_dict["transcript"]
        speed_of_speech = input_dict["speed_of_speech"]
        second_task_duration = (
            input_dict.get("second_task_duration", 0) if part == 2 else 0
        )
        if part == 2:
            return {
                "transcript": transcript,
                "speed_of_speech": speed_of_speech,
                "second_task_duration": second_task_duration,
            }
        else:
            return {
                "transcript": transcript,
                "speed_of_speech": speed_of_speech,
                "second_task_duration": 0,
            }

    return RunnableLambda(set_second_task_duration)


def construct_chain(self):

    part = 1

    set_lambda = create_set_lambda(part=part)
    analyzer = AnalyzerSingle(part=part)
    _feedback_chain = set_lambda | analyzer._feedback_chain
    return _feedback_chain


if __name__ == "__main__":

    client = Client()

    res = run_on_dataset(
        client,
        dataset_name="1PartFeedback",
        llm_or_chain_factory=construct_chain,
        project="ielts-test",
    )
