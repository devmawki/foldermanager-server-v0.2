import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = os.getenv("PROMPT")

gptModel = os.getenv("MODEL")
                  
class Request(BaseModel):
    userInput: str
    fileList: list[str]

@app.post("/chat")
def chat(req: Request):
    response = client.responses.create(
        model=gptModel,
        input=[{"role": "user", "content": prompt + req.userInput},
               {"role": "user", "content": "\n".join(req.fileList)}]
    )

    return {"result": response.output_text}
