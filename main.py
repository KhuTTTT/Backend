from fastapi import FastAPI, File, UploadFile
from make_quizz import make_sample, summary
import openai
import pts
import urllib3
from preprocessing import preprocess

http = urllib3.PoolManager()
app = FastAPI()

@app.get("/make_sample")
def gpt(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = make_sample(pdf_contents)
    preprocess(item)
    return {"item": item}


@app.get("/summary")
def gpt(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = summary(pdf_contents)
    return {"item": item}

@app.post("/make_sample_file")
async def create_file(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    items = make_sample(pdf_contents)
    preprocess(items)
    return {"item": item}

@app.post("/summary_file")
async def create_file2(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    item = summary(pdf_contents)
    return {"item": item}

