import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

renamePrompt = os.getenv("PROMPT_RENAME")
movePrompt = os.getenv("PROMPT_MOVE")

gptModel = os.getenv("MODEL")

class Request(BaseModel):
    userInput: str
    fileList: list[str]

@app.post("/rename")
def rename(req: Request):
    response = client.responses.create(
        model=gptModel,
        input=[{"role": "system", "content": renamePrompt + req.userInput},
               {"role": "user", "content": "\n".join(req.fileList)}]
    )

    return {"result": response.output_text}

@app.post("/move")
def move(req: Request):
    response = client.responses.create(
        model=gptModel,
        input=[{"role": "system", "content": movePrompt + req.userInput},
               {"role": "user", "content": "\n".join(req.fileList)}]
    )

    return {"result": response.output_text}
