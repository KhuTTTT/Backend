import re
import os
from dotenv import load_dotenv
from io import BytesIO
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def getallquestions():
    return supabase.table("question").select("*").execute().data

def getquestions(id_list):
    return supabase.table("question").select("*").in_("id", id_list).execute().data

def getquestion(id):
    return supabase.table("question").select("*").eq("id", id).execute().data

def getanswer(id):
    return supabase.table("answer").select("*").eq("question_id", id).execute().data

def getanswers(id_list):
    return supabase.table("answer").select("*").in_("question_id", id_list).execute().data

def getwrong(id):
    return supabase.table("wrong").select("*").eq("question_id", id).execute().data

def getwrongs(id_list):
    return supabase.table("wrong").select("*").in_("question_id", id_list).execute().data

def getdocument(id):
    return supabase.table("document").select("*").eq("id", id).execute().data

def getbydocument(id):
    return supabase.table("question").select("*").eq("document_id", id).execute().data

def getrandomquestion():
    return supabase.table("question").select("id").execute().data
