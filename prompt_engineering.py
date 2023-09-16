from utils import *

def prompt_engineering(page_content, question):
    model_input = question_utils(page_content, question)
    
    return model_input