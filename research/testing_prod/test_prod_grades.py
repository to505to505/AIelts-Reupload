from io import StringIO
import os

import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.getenv("PYTHONPATH"))

from src.services.analyzer import AnalyzerImpl


from research.grades_evaluators import final_evaluation

# Initializing grades_chain
analyzer = AnalyzerImpl()
_grade_chain = analyzer._grade_chain


dop_infa = analyzer.dop_infa
dataset = analyzer.dataset


if __name__ == "__main__":
    final_evaluation(
        chain=_grade_chain,
        experiment_prefix="testing_prod_version_full",
        dataset=dataset,
        dop_infa=dop_infa,
    )
