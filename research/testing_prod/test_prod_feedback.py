from io import StringIO
import os


import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../")))

from api.src.chains.feedback import build_feedback_chains
from api.src.services.llm_wrapper import LLMWrapper

os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["LANGSMITH_PROJECT"] = "ielts-test"

from langchain.smith.evaluation import run_on_dataset
from langsmith import evaluate, Client


def construct_chain(self):
    llm = LLMWrapper(test=True)
    return build_feedback_chains(llm, 0)['feedback_chain']

if __name__ == "__main__":

    client = Client()

    res = run_on_dataset(
        client,
        dataset_name="Feedback",
        llm_or_chain_factory=construct_chain,
        project="ielts-test",
    )
