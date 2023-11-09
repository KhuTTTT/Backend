import re
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def preprocess(items):
    print(items)
    pattern = r"\n\n"
    result = re.split(pattern, items[0])
    return_title = ""
    return_choices = []
    return_wrong_choices = []
    return_answer = ""
    print(result)

    for i in range(len(result)):
        if i % 2 == 0:
            question = result[i].split("\n")[0]
            choices = result[i].split("\n")[1:]
            for j in range(len(choices)):
                choices[j] = re.split(r"\d. ", choices[j])[1]
            return_title = re.split(r"Q\d+: ", question)[1]
            return_choices = choices
        else:
            return_answer = re.split(r"A\d+: \d+. ", result[i])[1]
            for l in return_choices:
                if(l != return_answer):
                    return_wrong_choices.append(l)

            #supabase.table("member").insert({"email": "sunwu5678@gmail.com", "password": "park13579@"}).execute()
            question = supabase.table("question").insert({"question": return_title, "chapter": "7", "document_id":1, "subject_id":1}).execute()
            print(question.data[0]["id"])
            question_id = question.data[0]["id"]
            for i in return_wrong_choices:
                wrongs = supabase.table("wrong").insert({"wrong": i, "question_id": question_id}).execute()
            answer = supabase.table("answer").insert({"answer": return_answer, "question_id": question_id}).execute()

            return_title = ""
            return_choices = []
            return_wrong_choices = []
            return_answer = ""