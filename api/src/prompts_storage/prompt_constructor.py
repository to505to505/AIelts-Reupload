from .prompts import part_dict, section_dict, first_extra_commentary, second_extra_commentary, third_extra_commentary, forth_extra_commentary
from langchain_core.prompts import PromptTemplate

from .ExtendedPromptTemplate import ExtendedPromptTemplate



def create_prompt( part: int = 0, section: str = 'lexical', scope: str = 'feedback', format_instructions_parser: str = ''):
    """
    Parameters
    ----------
    part : int,
        Defines the part of the speaking test, from 0 to 4.
        - 0: full test
        - 1: first part
        etc.

        
    
        section : str,
        Defines what is graded in this prompt
        - 'lexical'
        - 'grammar'
        - 'coherence'

    
    scope : str,
    Defines is it mistakes or feedback or checking for relevance (gibberish)
    - 'mistakes'
    - 'feedback'
    - 'gibberish'


    
    Comments below before self.text are intermediate comments to add. Their number mean their position in the prompt. F.e. comment_35 - comment 3 and a half between 
    third and forth big commentaries.
    """ 

    
    if scope =='gibberish':
        return PromptTemplate.from_template(template = """You are a program that grades the IELTS speaking exam.
                                                    You get a transcript of {part_introduction} and you need to detect whether it is a valid student's speaking test transcript or just some gibberish, unrelated to questions
    asked by the examiner. Below you will see a transcript of the student's speaking. 
    Be aware that recordings, and therefore transcripts, might be cropped at the beginning and/or at the end.
    Phrases in parentheses are teacher's questions, so don't consider them part of the student's speaking!                                             

    Transcript: \n {transcript}. END OF THE TRANSCRIPT. \n\n
                                                    
    RETURN JUST ONE WORD: yes or no (if the transcript is relevant to the questions asked by the examiner return yes and no otherwise)
                                                    """, partial_variables ={"part_introduction" : part_dict[part]} ) 
    
    comment_35 = "" 
    if section == 'coherence' and (part == 0 or part == 2):
        comment_35 = """Also consider the duration of the student's second task (monologue) in the feedback. 
    The student was speaking for {second_task_duration} seconds, while the optimal time for the answer is 90 - 125 seconds."""

    
    return ExtendedPromptTemplate.from_template(template= """
                                        
    You are a program that grades the IELTS speaking exam. You get a transcript of {part_introduction} and you need to {section_introduction}
    {first_commentary} 
    Below you will see a transcript of the student's speaking. 
    Be aware that recordings, and therefore transcripts, might be cropped at the beginning and/or at the end.
    Phrases in parentheses are teacher's questions, so don't consider them part of the student's speaking! 
    {second_commentary}
    \n {transcript}. \n\n [END OF THE TRANSCRIPT] \n    
    {third_commentary} 
                                                
    {comment_35}
                                                
    {forth_commentary}
                                                
    {format_instructions_parser}
    """, partial_variables = {"part_introduction" : part_dict[part], "section_introduction":section_dict[(section, scope)],
                            "first_commentary":  first_extra_commentary[(section, scope, part)], "second_commentary": second_extra_commentary[part],
                                "third_commentary": third_extra_commentary[(section, scope)], "comment_35": comment_35,
                                "forth_commentary": forth_extra_commentary[scope], "format_instructions_parser":  format_instructions_parser })

    
    
def mistakes_parser_prompt(part):
    """ part = 'lexical'
        OR part = 'grammar'"""

    if part=='lexical':
        return PromptTemplate.from_template(template = "You are an AI assistant that parses answers of another LLM into the right format. TO be precise, another model found mistakes in the text, and you are parsing them into the right format. Use the specified format instructions.\n The answer of the model: {lexical_mistakes_unformatted} \n\n END OF THE ANSWER OF THE MODEL.")
    else:
        return PromptTemplate.from_template(template = "You are an AI assistant that parses answers of another LLM into the right format. TO be precise, another model found mistakes in the text, and you are parsing them into the right format. Use the specified format instructions.\n The answer of the model: {grammar_mistakes_unformatted} \n\n END OF THE ANSWER OF THE MODEL.")