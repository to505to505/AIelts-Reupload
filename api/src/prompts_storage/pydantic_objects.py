from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


# dotenv.load_dotenv()
# sys.path.append(os.getenv("PYTHONPATH"))

# from .JsonOutputParserReasoner import JsonOutputParserReasoner





# !!! In this file only models that are used in chains are presented !!!



# Grades model

class Grades(BaseModel):
    """
    Just putting grades
    float grades for 3 IETLS criteria. NEVER leave these fields empty and NEVER put null or none values.
    """

    Arguments: str = Field(
        description="Give sufficient and concise argumentation for choosen grades. "
    )
    Coherence: float = Field(
        description="Grade for Fluency and Coherence category. Just the grade! If you can't put any grade, just put 0. Always put something here. NEVER leave this field as None or null. "
    )
    Lexical: float = Field(
        description="Grade for Lexical Resource category. Just the grade! If you can't put any grade, just put 0. Always put something here. NEVER leave this field as None or null. "
    )
    Grammar: float = Field(
        description="Grade for Grammatical range and accuracy category. Just the grade! If you can't put any grade, just put 0. Alwaya put something here. NEVER leave this field as None or null."
    )


# Selected examples model
    
class SelectedExamples(BaseModel):
    ''' Put the ids of selected examples here.'''
    Examples_ids: list[int] = Field(description = "A list of ids (int) of selected useful examples here")
    Comments: str = Field(description = "Argumentation for selection")
    



### MISTAKES AND FEEDBACK MODELS

class GrammarMistakesFeedback(BaseModel):
    """Write down all the grammar mistakes in this format. Also give an overall commentary and advice on grammar."""

    ActualVersions: list[str] = Field(
        description="List all of the grammar mistakes you have found in the text in chronological order. "
    )
    TypeOfMistake: list[str] = Field(
        description="List types of mistakes for all mistakes you have found in chronological order."
    )
    CorrectedVersions: list[str] = Field(
        description="List corrected versions (rewrited phrases) of mistakes you have found in the text in chronological order."
    )
    CommentaryGrammar: str = Field(
        description="Overall commentary on gramnatical range and accuracy and advice on improvement."
    )

class LexicalMistakesFeedback(BaseModel):
    """
    Write down lexically unsuccessful phrases and their rephrased versions.
    Also provide an overall commentary and advice on lexical resource of the student's transcript.
    """

    OriginalSentences: list[str] = Field(
        description="List of lexically unsuccessful phrases from the text."
    )
    RephrasedSentences: list[str] = Field(
        description="List of improved versions of the lexically unsuccessful phrases."
    )
    CommentaryLexical: str = Field(
        description="Justification for the score, detailed commentary, and suggestions for improvement (include a link to an article explaining the rule or practical tips on how to improve)."
    )

class CoherenceMistakesFeedback(BaseModel):
    """Provide an overall commentary on the student's fluency and coherence."""

    CommentaryCoherence: str = Field(
        description="Justification for the score, detailed commentary, recommendations on structuring the answer, presence or absence of logical errors, and suggestions for improvement (what to study, what to read, what to pay attention to, what to repeat to avoid making mistakes in the future)."
    )



### JUST MISTAKES MODELS
    
class GrammarMistakes(BaseModel):
    """Write down all the grammar mistakes in this format."""
    ActualVersions: list[str] = Field(
        description="List all of the grammar mistakes you have found in the text in chronological order. "
    )
    TypeOfMistake: list[str] = Field(
        description="List types of mistakes for all mistakes you have found in chronological order."
    )
    CorrectedVersions: list[str] = Field(
        description="List corrected versions (rewrited phrases) of mistakes you have found in the text in chronological order."
    )

GrammarMistakesParser = JsonOutputParser(pydantic_object = GrammarMistakes)


class LexicalMistakes(BaseModel):
    """
    Write down lexically unsuccessful phrases and their rephrased versions.
   
    """
    OriginalSentences: list[str] = Field(
        description="List of lexically unsuccessful phrases from the text."
    )
    RephrasedSentences: list[str] = Field(
        description="List of improved versions of the lexically unsuccessful phrases."
    )

LexicalMistakesParser = JsonOutputParser(pydantic_object = LexicalMistakes)
  


if __name__ == "__main__":
    print(type(GrammarMistakesParser.get_format_instructions()))