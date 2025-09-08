
import re
import os

import re
from dotenv import load_dotenv
import sys
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))
# Mistakes and feedback by category models
from src.prompts_storage.pydantic_objects import (
    GrammarMistakesFeedback,
    LexicalMistakesFeedback,
)





def add_indices_mistakes(data, text):
    """Arrange erors in the right order in the text"""

    phrases_grammar = data["grammar"].ActualVersions
    phrases_lexical = data["lexical"].OriginalSentences

    # Получаем список фраз из ActualVersions

    indecies_grammar = []
    indecies_lexical = []

    # Для каждой фразы ищем все её вхождения в тексте
    for phrase in phrases_grammar:
        # Экранируем специальные символы в фразе для точного поиска
        pattern = re.escape(phrase)
        match = re.search(pattern, text)
        # Находим все совпадения и сохраняем их начальные индексы
        if match:
            indecies_grammar.append(match.start())
        else:
            indecies_grammar.append(
                indecies_grammar[-1] + 1 if len(indecies_grammar) > 0 else 0
            )

    for phrase in phrases_lexical:
        # Экранируем специальные символы в фразе для точного поиска
        pattern = re.escape(phrase)
        match = re.search(pattern, text)
        # Находим все совпадения и сохраняем их начальные индексы
        if match:
            indecies_lexical.append(match.start())
        else:
            indecies_lexical.append(
                indecies_lexical[-1] + 1 if len(indecies_lexical) > 0 else 0
            )

    # Добавляем поле 'indecies' в data['grammar_feedback']

    return indecies_grammar, indecies_lexical


def concat_parts(
    Part1_text: str,
    Part2_text: str,
    Part3_text: str,
) -> str:
    """Concatenates all parts of a text and their questions.

    Partx_questions: list[Tuple[offset, question]]
    TimeStampsPartx: just the dict you get from transcribe() : dict['time_stamps']

    time_measure: 's' - seconds or 'ms' - miliseconds

     Returns just a string with the full text with questions.

    """

    full = (
        "  [ Part 1. Student and teacher's dialogue: ] \n"
        + Part1_text
        + "\n [ Part 2. Student answering the 2nd part open-ended question: ] \n"
        + Part2_text
        + "\n [ Part 3. Student and teacher's dialogue: ] \n"
        + Part3_text
    )

    return full






# Functions to parse mistakes and feedback


def parse_grammar_feedback(all_args: tuple) -> GrammarMistakesFeedback:

    return GrammarMistakesFeedback(
        ActualVersions=all_args[1].ActualVersions,
        TypeOfMistake=all_args[1].TypeOfMistake,
        CorrectedVersions=all_args[1].CorrectedVersions,
        CommentaryGrammar=all_args[0].content,
    )


def parse_lexical_feedback(all_args: tuple) -> LexicalMistakesFeedback:

    return LexicalMistakesFeedback(
        OriginalSentences=all_args[1].OriginalSentences,
        RephrasedSentences=all_args[1].RephrasedSentences,
        CommentaryLexical=all_args[0].content,
    )


def add_indices_mistakes(data, text):
    """Arrange erors in the right order in the text"""

    phrases_grammar = data["grammar"].ActualVersions
    phrases_lexical = data["lexical"].OriginalSentences

    # Получаем список фраз из ActualVersions

    indecies_grammar = []
    indecies_lexical = []

    # Для каждой фразы ищем все её вхождения в тексте
    for phrase in phrases_grammar:
        # Экранируем специальные символы в фразе для точного поиска
        pattern = re.escape(phrase)
        match = re.search(pattern, text)
        # Находим все совпадения и сохраняем их начальные индексы
        if match:
            indecies_grammar.append(match.start())
        else:
            indecies_grammar.append(
                indecies_grammar[-1] + 1 if len(indecies_grammar) > 0 else 0
            )

    for phrase in phrases_lexical:
        # Экранируем специальные символы в фразе для точного поиска
        pattern = re.escape(phrase)
        match = re.search(pattern, text)
        # Находим все совпадения и сохраняем их начальные индексы
        if match:
            indecies_lexical.append(match.start())
        else:
            indecies_lexical.append(
                indecies_lexical[-1] + 1 if len(indecies_lexical) > 0 else 0
            )

    # Добавляем поле 'indecies' в data['grammar_feedback']

    return indecies_grammar, indecies_lexical


def get_content_from_the_message(message):
    return message.content
