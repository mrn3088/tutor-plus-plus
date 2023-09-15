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
