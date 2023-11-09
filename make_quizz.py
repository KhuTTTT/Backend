import openai
import pts
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def make_sample(contents):
    print("지피티 실행!")
    model = "gpt-3.5-turbo"
    # 질문 작성하기
    sentence_type =  "[주어진 텍스트를 기반으로 5지 선다 문제를 10개 만들어줘.]"
    query = sentence_type+contents
    print("쿼리")
    # 메시지 설정하기
    print(query)
    messages = [
            {"role": "system", "content": """You are a college professor teaching students through a given text. You must write a five-choice test question based on the concepts in the given text. Please provide appropriate test questions. Please also provide answers to the test questions.

The output format is as follows.

Output Format:

Q1: content of question1

A1: content of answer1 as single number

...."""},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    print("호출 성공")
    answer = response['choices'][0]['message']['content']
    return answer


def summary(contents):
    print("지피티 실행!")
    model = "gpt-3.5-turbo"
    # 질문 작성하기
    sentence_type =  "[주어진 텍스트를 기반으로 요약해줘]"
    query = sentence_type+contents
    print("쿼리")
    # 메시지 설정하기
    print(query)
    messages = [
            {"role": "system", "content": "You are a college professor teaching students through a given text. You have to write summary based given text."},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    print("호출 성공")
    answer = response['choices'][0]['message']['content']
    return answer
