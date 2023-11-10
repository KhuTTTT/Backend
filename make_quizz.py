import openai
import pts
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def string_prepeocess(quizz):
    quizz_list = quizz.split("\n")
    question_no = ['A1:','A2:','A3:','A4:','A5:','A6:','A7:','A8:']
    for i in range(len(quizz_list)):
        #print(quizz_list[i])
        for j in question_no:
            if j in quizz_list[i]:
                quizz_list[i] = quizz_list[i][:5]
    return '\n'.join(quizz_list)

def generate_question(contents):
    print("지피티 실행!")
    model = "gpt-3.5-turbo"
    # 질문 작성하기
    sentence_type =  "[주어진 텍스트를 기반으로 5지 선다 문제를 5개 만들어줘.]"
    query = sentence_type+contents
    print("쿼리")
    # 메시지 설정하기
    #print(query)
    messages = [
            {"role": "system", "content": """You are a college professor teaching students through a given text. You must write a five-choice test question based on the concepts in the given text. Please provide appropriate 5 test questions. Please also provide answers to the test questions.
The output format is as follows.
Output Format:
Q1: content of question1
1. Option1 of Q1
2. Option2 of Q1
3. Option3 of Q1
4. Option4 of Q1
5. Option5 of Q1

A1: answer number of Q1
             
Q2: content of question2
1. Option1 of Q2
2. Option2 of Q2
3. Option3 of Q2
4. Option4 of Q2
5. Option5 of Q2

A2: answer number of Q2
             
Q3: content of question3
1. Option1 of Q3
2. Option2 of Q3
3. Option3 of Q3
4. Option4 of Q3
5. Option5 of Q3

A3: answer number of Q3
             
Q4: content of question4
1. Option1 of Q4
2. Option2 of Q4
3. Option3 of Q4
4. Option4 of Q4
5. Option5 of Q4

A4: answer number of Q4
             
Q5: content of question5
1. Option1 of Q5
2. Option2 of Q5
3. Option3 of Q5
4. Option4 of Q5
5. Option5 of Q5

A5: answer number of Q5
"""},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    print("호출 성공")
    answer = response['choices'][0]['message']['content']
    answer = string_prepeocess(answer)
    return answer


def summary(contents):
    print("지피티 실행!")
    model = "gpt-3.5-turbo"
    # 질문 작성하기
    sentence_type =  "[주어진 텍스트를 기반으로 요약해줘]"
    query = sentence_type+contents
    print("쿼리")
    # 메시지 설정하기
    #print(query)
    messages = [
            {"role": "system", "content": """You are a graduate student. I have to read the paper and summarize it. Given text, your job is to summarize that text with text extracted from the paper. It must be printed in the format below.

Title: content of title

Author: content of Author

Introduction: content of Introduction

Abstract: content of abstract

How to expriment: content of how to expriment

Main content1: content of main content1
             
Main content2: content of main content2
            
Main content3: content of main content3

Conclusion: content of conclusion"""},
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
