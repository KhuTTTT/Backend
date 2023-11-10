import re
import os
from dotenv import load_dotenv
from io import BytesIO
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
all_questions = []


def preprocess(items, document_id):
    #print(items)
    pattern = r"\n\n"
    result = re.split(pattern, items)
    return_title = ""
    return_choices = []
    return_wrong_choices = []
    return_answer = ""
    #print(result)

    for i in range(len(result)):
        if i % 2 == 0:
            question = result[i].split("\n")[0]
            choices = result[i].split("\n")[1:]
            for j in range(len(choices)):
                choices[j] = re.split(r"\d. ", choices[j])[1].replace("\n", "")
            return_title = re.split(r"Q\d+: ", question)[1].strip()
            return_choices = choices
        else:
            #print("RESULT: ")
            #print(result[i])
            return_answer = re.split(r"A\d+: ", result[i])[1]
            
            #print("RETURN_CHOICES: ")
            #print(return_choices)
            
            for k in range(1,len(return_choices)+1):
                if(str(k) != return_answer):
                    return_wrong_choices.append(return_choices[k-1])

            return_answer = choices[int(return_answer)-1]
            #print("ANSWER: ")
            #print(return_answer)

            #print("TITLE: ")
            #print(return_title)
            #print("CHOICES: ")
            #print(return_wrong_choices)

            supabase.table("member").insert({"email": "sunwu5678@gmail.com", "password": "park13579@"}).execute()
            question = supabase.table("question").insert({"question": return_title, "chapter": "7", "document_id":document_id, "subject_id":1}).execute()
            question_id = question.data[0]["id"]
            all_questions.append(question_id)
            for i in return_wrong_choices:
                wrongs = supabase.table("wrong").insert({"wrong": i, "question_id": question_id}).execute()
            answer = supabase.table("answer").insert({"answer": return_answer, "question_id": question_id}).execute()

            return_title = ""
            return_choices = []
            return_wrong_choices = []
            return_answer = ""

    return all_questions