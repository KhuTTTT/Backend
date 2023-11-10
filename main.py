from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
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
import concurrent.futures
import asyncio


http = urllib3.PoolManager()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##URL 로 문제들 만들기
@app.get("/make_sample")
async def gpt_make_sample(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = generate_question(pdf_contents)
    itmes = preprocess(item)
    return {"item": itmes}

##URL로 요약문 만들기
@app.get("/summary")
async def gpt_summary(url: str):
    response = http.request('GET', url)
    pdf_contents = pts.PdfToString(response.data)
    item = summary(pdf_contents)
    return {"item": item}

@app.post("/create_file_and_ppt")
async def create_file_and_ppt(file: bytes = File()):
    file_result, ppt_result = await asyncio.gather(create_file(file), create_ppt(file))
    return {"file_result": file_result, "ppt_result": ppt_result}


## 파일로 문제들 만들기
@app.post("/create_file")
async def create_file(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    items = generate_question(pdf_contents)
    input_list = preprocess(items)

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

## 파일로 요약문 만들기
@app.post("/summary_file")
async def summary_file(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    item = summary(pdf_contents)
    return {"item": item}

##ppt 만들기
@app.post("/ppt")
async def create_ppt(file: bytes = File()):
    ppt_generator = PPT()
    ppt = ppt_generator.create_presentation(file)
    return {"ppt": ppt["res"], "image": ppt["res_image"]}

@app.post("/register")
async def register(file: bytes = File()):
    pdf_contents = pts.PdfToString(file)
    ppt_generator = PPT()
    ppt = ppt_generator.create_presentation(file)
    items = generate_question(pdf_contents)
    itmes = preprocess(items, ppt["document_id"])

    return {"item": itmes}

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

@app.get("/document/{id}")
async def get_document(id):
    datas = getbydocument(id)
    input_list = []
    for data in datas:
        input_list.append(data["id"])
    
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

@app.get("/answerandwrong/{id}")
async def getanswerandwrong(id):
    answer = getanswer(id)
    wrong = getwrong(id)
    #print(answer)
    #print(wrong)
    return {"answer": answer, "wrong" : wrong}

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

@app.get("/randomquestion5")
async def get_random_question5():
    data = getrandomquestion()
    number_list = random.sample(data, 5)
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