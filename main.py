from fastapi import FastAPI, File, UploadFile
from make_quizz import generate_question, summary
import openai
import pts
import urllib3
import make_quizz
from preprocessing import preprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from make_ppt import PPT

http = urllib3.PoolManager()
app = FastAPI()

@app.get("/make_sample")
def gpt(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = generate_question(pdf_contents)
    itmes = preprocess(item)
    return {"item": itmes}

@app.get("/summary")
def gpt(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = summary(pdf_contents)
    return {"item": item}

@app.post("/make_sample_file")
async def create_file(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    items = generate_question(pdf_contents)
    itmes = preprocess(items)
    return {"item": itmes}

@app.post("/summary_file")
async def create_file2(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    item = summary(pdf_contents)
    return {"item": item}

@app.post("/ppt")
async def create_ppt(url: str):
    response = http.request('GET', url)
    ppt_generator = PPT()
    ppt = ppt_generator.create_presentation(response.data)
    return {"ppt": ppt}