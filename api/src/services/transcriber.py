import json
from pocketbase.client import FileUpload
import asyncio
from io import BytesIO
import os

import re

import httpx
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.services.analyzer import analyze
from src.config.pb import pb
from src.helpers.transcriber_helpers import is_triple, find_word_indices, concate_with_offset_list, clean_html_and_preserve_br, convert_to_mp3

from src.models import Answer, TranscriptOutput, Question, TimeStampWord

from src.services.speech2text_wrapper import IELTSWhisper


       

async def transcribe_audio(answer_id: str, attempt_id: str, test = False) -> TranscriptOutput:
    """
    Основная функция транскрибирования.
    Загружает аудио по URL, конвертирует его в wav и передаёт в OPENAI.
    """


    # инициилизируем speech 2 text модель 
    speech2text = IELTSWhisper(prompt = """
                                Umm, let me think like, hmm... Okay, here's what I'm, like, thinking.
                                So, the issue here is, obviously, lays ummm... within the domain.
                                Hello, and what do you think about these?
                                """, 
                                temperature = 0.5)
                               
                               
    # Получаем запись ответа
    answer = pb.collection("answers").get_one(answer_id, {"expand": "task"})

    questionsOffsets = answer.question_offsets

    # составляем список вопросов
    task = answer.expand["task"]
    if task.part == 2:
        list_questions = [Question(content=task.questions, offset=0)]
    else:
        list_questions = []
        questions_html = task.questions
        li_pattern = r"<li[^>]*>(.*?)<\/li>"
        li_matches = re.findall(li_pattern, questions_html, re.DOTALL)
        
        #если юзер не успел ответить на все вопросы, то обрезаем список вопросов
        if len(li_matches) > len(questionsOffsets):
            li_matches = li_matches[:len(questionsOffsets)]
    
        for index, li_content in enumerate(li_matches):
            clean_content = re.sub(r"<[^>]+>", "", li_content).strip()
            if clean_content:
                list_questions.append(
                    Question(content=clean_content, offset=questionsOffsets[index])
                )

    # Получаем аудиофайл
    audio_url = pb.get_file_url(answer, answer.audio)
    print("LOADING AUDIO FILE...: ", audio_url)
    async with httpx.AsyncClient(timeout=60 * 5) as client:
        response = await client.get(audio_url)
        response.raise_for_status()


    # определяем расширение файла
    extension = os.path.splitext(audio_url.split("?")[0])[-1]
    if not extension:
        raise ValueError("File extension could not be determined from URL.")
    print(f"DETECTED EXTENSION: {extension}")

    # Загружаем аудиоданные в BytesIO
    audio_file = BytesIO(response.content)
    audio_file.name = f"audio{extension}"

    # Конвертируем в wav (блокирующая операция обернута в asyncio.to_thread)
    print("Converting audio file to wav format...")
    mp3_file = await asyncio.to_thread(convert_to_mp3, audio_file, extension)
    print("Conversion complete. Sending wav file to OPENAI...")


    # происходит транскрибация
    transcription = await speech2text.get_transcript(mp3_file)

    print("TRANSCRIPTION: ", transcription)



    ### Подсчёт букв, не являющихся тройками для более точной оценки скорости речи 
    counter = 0
    for word in transcription.words:
        if not is_triple(word):
            counter += 1

    text_new = ""


    # забираем таймстемпы
    time_stamps = [
        TimeStampWord(start=word.start, end=word.end, word=word.word)
        for word in transcription.words
    ]

    # Если это вторая часть (предполагается, что list_questions определён вне этого фрагмента)
    if len(list_questions) == 1:
        clean_text = clean_html_and_preserve_br(list_questions[0].content)
        text_new = f"""<strong><p style="color: blue;">{clean_text}</p></strong>{transcription.text}"""
    else:
        text_new = transcription.text.replace("\n", "")
        list_for_offset_index = find_word_indices(time_stamps, list_questions)
        text_new = concate_with_offset_list(
            list_for_offset_index, text_new, list_questions
        )

    file_path = f"/tmp/{answer_id}.mp3"


    with open(file_path, "wb") as f:
        f.write(mp3_file.getvalue())


    with open(file_path, "rb") as f:
        pb.collection("answers").update(
            answer_id,
            {
                "content": text_new,
                "audio": FileUpload(("audio.mp3", f)),
                "temp": json.dumps(
                    {
                        "duration": transcription.duration,
                        "speed": counter / transcription.duration,
                        "time_stamps": [ts.model_dump() for ts in time_stamps],
                    }
                ),
            },
        )

    attempt = pb.collection("attempts").get_one(
        attempt_id, {"expand": "answers,answers.task"}
    )
    attempt_answers = attempt.expand["answers"]
  


    # Eсли все ответы в попытке заполнены, то анализируем!!
    if len([a for a in attempt_answers if a.content]) == len(attempt_answers):
        
        answers = []
        total_speed = 0
        for a in attempt_answers:
            
            answers.append(
                Answer(
                    text=a.content,
                    part=a.expand["task"].part,
                    duration_seconds=float(a.temp["duration"]),
                )
            )
            total_speed += a.temp["speed"]
        avg_speed = total_speed / len(attempt_answers)

        if len(attempt_answers) == 3:
            feedback = await analyze(answers, avg_speed, 0, attempt_id)
    
        else:
            feedback = await analyze(answers, avg_speed, task.part, attempt_id)


        # вернулась ошибка
        if (isinstance(feedback, dict) and 'error' in feedback): 
            pb.collection("attempts").update(attempt_id, {"result": {"error": {'code': feedback['error']['code'], "message": feedback['error']['message']}}})


        # все нормально
        else:
            pb.collection("attempts").update(
                attempt_id, {"result": {"feedback": feedback.model_dump()}}
            )

            for a in attempt_answers:
                pb.collection("answers").update(a.id, {"temp": None})

        # если это тест, то возвращаем feedback и очищаем поля контента, чтобы можно было повторно запустить процессинг данных примеров для тестров
        if test:
            for a in attempt_answers:
                pb.collection("answers").update(a.id, {"content": None})

            return feedback