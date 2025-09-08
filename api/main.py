import os
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware


load_dotenv(".env")
import sys

sys.path.append(os.getenv("PYTHONPATH"))


from src.services.transcriber import transcribe_audio
from src.config.sheduler import scheduler

app = FastAPI()

allowed_origin = os.getenv("ORIGIN")
if allowed_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[allowed_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/api/audio/{answer_id}/transcribe")
async def transcribe(
    answer_id: str,
    attempt_id: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(transcribe_audio, answer_id, attempt_id)
    return Response(status_code=202)


if __name__ == "__main__":
    import uvicorn

    load_dotenv("../.env")
    scheduler.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
