from src.models import Answer, Question, TimeStampWord
import re

from io import BytesIO
from pydub import AudioSegment

def is_triple(s: str) -> bool:
    if "mmm" in s or "aaa" in s:
        return True
    return False



def concate_with_offset_list(offset_list: list, text: str, questions: list):
    text = text.strip()
    text_list = text.split(" ")

    words_with_dash = []
    for count, word in enumerate(text_list):
        if "-" in word:
            words_with_dash.append(count)

    for count, i in enumerate(offset_list):

        dash_counter = count_dashes(words_with_dash, i)
        if count == 0:
            question_with_brackets = f"""<strong><font color="blue">{questions[count].content}</font></strong>"""
        else:
            question_with_brackets = f"""<br><strong><font color="blue">{questions[count].content}</font></strong>"""
        if i == 0:

            text_list.insert(count, question_with_brackets)

        else:

            text_list.insert(i + count + 1 - dash_counter, question_with_brackets)

    text = " ".join(text_list)
    return text


def count_dashes(words_with_dashes, index):
    if len(words_with_dashes) == 0:
        return 0
    count = 0
    for i in words_with_dashes:
        if index >= i:

            count += 1

    return count


def find_word_indices(
    time_stamp_words: list[TimeStampWord], questions_list: list[Question]
):
    """
    Check where the button click is in the words list.
    """

    list_for_offset_index = []

    for q in questions_list:
        list_for_offset_index.append(word_index(time_stamp_words, q.offset))

    return list_for_offset_index


def word_index(words: list[TimeStampWord], offset: float):
    if not len(words):
        return 0

    for i in range(len(words)):

        if i == 0 and offset <= words[0].start:
            return 0

        if words[i].start <= offset <= words[i].end:
            return i

        elif i < len(words) - 1 and words[i].end <= offset <= words[i + 1].start:
            return i

    return i - 1

def answer_to_transcribe(answer: Answer, time_measure: str, part: int) -> str:
    text = answer.text
    if part in (1, 3) and time_measure == "ms":
        for t in answer.time_stamps:
            t["start"] = t["start"] / 1000
            t["end"] = t["end"] / 1000

    if part in (1, 3):
        word_indexes = find_word_indices(answer.time_stamps, answer.questions)
        text = text.replace("\n", " ")

        text_list = text.split(" ")
        for count, i in enumerate(word_indexes):
            question_with_brackets = f"({answer.questions[count][0]})"
            text_list.insert(i + 1, question_with_brackets)
        text = " ".join(text_list)

    match part:
        case 1:
            part_prefix = "Part 1 (student and teacher's dialogue):"
        case 2:
            part_prefix = "Part 2 (student answering the 2nd part open question):"
        case 3:
            part_prefix = "Part 3 (student and teacher's dialogue):"

    return f"{part_prefix}\n{text}\n"





def clean_html_and_preserve_br(text):
    """Удаляет все HTML-теги, кроме <br> и <br/>, заменяет \n на <br>, и убирает тройные <br>, оставляя двойные."""
    # Удаляем все HTML-теги, кроме <br> и <br/>
    clean_text = re.sub(r"<(?!br\s*/?)[^>]+>", "", text)
    # Заменяем \n на <br>
    clean_text = clean_text.replace("\n", "<br>")
    # Убираем тройные и более подряд идущие <br>, оставляя максимум два подряд
    clean_text = re.sub(r"(<br\s*/?>\s*){3,}", "<br><br>", clean_text)
    return clean_text.strip()



def clean_html_and_preserve_br(text):
    """Удаляет все HTML-теги, кроме <br> и <br/>, заменяет \n на <br>, и убирает тройные <br>, оставляя двойные."""
    # Удаляем все HTML-теги, кроме <br> и <br/>
    clean_text = re.sub(r"<(?!br\s*/?)[^>]+>", "", text)
    # Заменяем \n на <br>
    clean_text = clean_text.replace("\n", "<br>")
    # Убираем тройные и более подряд идущие <br>, оставляя максимум два подряд
    clean_text = re.sub(r"(<br\s*/?>\s*){3,}", "<br><br>", clean_text)
    return clean_text.strip()

def convert_to_mp3(input_file: BytesIO, extension: str) -> BytesIO:
    """
    Конвертирует аудио файл в формат mp3 используя pydub.
    """
    input_file.seek(0)

    file_format = extension.lstrip(".").lower()
    audio = AudioSegment.from_file(input_file, format=file_format)

    if audio.duration_seconds > 1200:
        raise ValueError("Длительность аудиофайла превышает 20 минут")

    output_file = BytesIO()
    audio.export(output_file, format="mp3")
    output_file.seek(0)
    output_file.name = "audio.mp3"
    return output_file
