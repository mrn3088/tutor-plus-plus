# -*- coding:utf-8 -*-

from model_inference import *
from utils import *
from academic_integrity_test import *
from prompt_engineering import *
from question_postprocessing import *
from search import *
from similarity_test import *
from model_inference_new import *

from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


def query(db_videos_coarse, db_books_coarse, db_videos, db_books, question):

    page_content_video_coarse, metadata_video_coarse, score_video = search_coarse(question , db_videos_coarse)

    page_content_book_coarse, metadata_book_coarse, score_book = search_coarse(question, db_books_coarse)
    
    page_content_video, metadata_video, score_video = search_fine(question , db_videos, dict(video_name=metadata_video_coarse['video_name']))

    page_content_book, metadata_book, score_book = search_fine(question, db_books, dict(file_name=metadata_book_coarse['file_name']))
        
    page_content = concat_page_content(page_content_book, page_content_video)
    
    model_input = prompt_engineering(page_content, question)
    
    model_output = model_inference_new(model_input)
    
    return question_postprocessing(model_output, question, metadata_book, metadata_video, score_book, score_video)
     
