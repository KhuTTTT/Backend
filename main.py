from fastapi import FastAPI, File, UploadFile
from make_quizz import *
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
from io import BytesIO
from service import *
import random

http = urllib3.PoolManager()
app = FastAPI()

##URL 로 문제들 만들기
@app.get("/make_sample")
def gpt_make_sample(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = generate_question(pdf_contents)
    itmes = preprocess(item)
    return {"item": itmes}

##URL로 요약문 만들기
@app.get("/summary")
def gpt_summary(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = summary(pdf_contents)
    return {"item": item}


## 파일로 문제들 만들기
@app.post("/create_file")
async def create_file(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    items = generate_question(pdf_contents)
    itmes = preprocess(items)
    return {"item": itmes}

## 파일로 요약문 만들기
@app.post("/summary_file")
async def summary_file(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    item = summary(pdf_contents)
    return {"item": item}

## 
@app.post("/ppt")
async def create_ppt(url: str):
    response = http.request('GET', url)
    ppt_generator = PPT()
    ppt = ppt_generator.create_presentation(response.data)
    return {"ppt": ppt}

@app.get("/questions/all")
async def get_questions():
    data = getallquestions()
    return {"questions": data}

@app.get("/questions/{id}")
async def get_question(id):
    data = getquestion(id)
    return {"question": data}

@app.get("/questions")
async def get_questions(id1: str, id2:str, id3:str):
    data = getquestions(id1, id2, id3)
    return {"question": data}

@app.get("/answerandwrong/{id}")
async def getanswerandwrong(id):
    answer = getanswer(id)
    wrong = getwrong(id)
    return {"answer": answer, "wrong" : wrong}

@app.get("/documents/{id}")
async def get_document(id):
    data = getdocument(id)
    return {"document": data}

@app.get("/randomquestion")
async def get_random_question():
    data = getrandomquestion()
    number_list = random.sample(data, 3)
    input_list = []

    for i in number_list:
        input_list.append(i["id"])

    questions = getquestions(input_list)
    answers = getanswers(input_list)
    wrongs = getwrongs(input_list)
    return_json = {}    

    for id in input_list:
        for i in questions:
            if id == i["id"]:
                i["answer"] = []
                i["wrong"] = []
                for j in answers:
                    if id == j["question_id"]:
                        i["answer"].append(j["answer"])
                for k in wrongs:
                    if id == k["question_id"]:
                        i["wrong"].append(k["wrong"])
                return_json[id] = i

    return {"input": return_json}