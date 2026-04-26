import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """Each line is one file or folder.

Rules:
- Keep the EXACT same number of lines
- Keep the EXACT same order
- Do NOT reorder, remove, or add lines
- Do NOT modify .exe file

- A line with an extension (e.g. .exe, .zip, .txt) is a file
- A line with NO extension is a folder

- Only modify names according to the User Command
- Do NOT modify anything else
- Do NOT modify the file extension (e.g. .exe, .zip, .txt)

Output ONLY the final list. No explanations.
Instruction : """

class Request(BaseModel):
    userInput: str
    fileList: list[str]

@app.post("/chat")
def chat(req: Request):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{"role": "user", "content": prompt + req.userInput},
               {"role": "user", "content": "\n".join(req.fileList)}]
    )

    return {"result": response.output_text}