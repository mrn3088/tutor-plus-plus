import requests
import json
import hashlib
import time


#问答题
def question_utils(input, question):
    return {
        "input":input,
        "prompt":"问答",
        "question":question,
        "<ans>":"",
    }
    
def sec_to_min(seconds):
    return seconds // 60, int(seconds) % 60

def concat_page_content(page_content_books, page_content_videos):
    return page_content_books+"\n"+page_content_videos