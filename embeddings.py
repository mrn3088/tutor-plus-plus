from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

import pdfplumber
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from pathlib import Path

embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")

def get_pdf_embedding(pdf_path_list):
    list_of_documents = []
    for idx, pdf_path in enumerate(pdf_path_list):
        with pdfplumber.open(pdf_path) as pdf:
            path = Path(pdf_path)
            filename = path.name
            text = ""
            for i, page in enumerate(pdf.pages):
                text += page.extract_text()
            list_of_documents.append(Document(page_content=text, metadata=dict(file_name=filename, pdf_num=idx)))
    return FAISS.from_documents(list_of_documents, embeddings)   

def get_pdf_embedding_paging(pdf_path_list):
    list_of_documents = []
    for idx, pdf_path in enumerate(pdf_path_list):
        with pdfplumber.open(pdf_path) as pdf:
            path = Path(pdf_path)
            filename = path.name
            for i, page in enumerate(pdf.pages):
                list_of_documents.append(Document(page_content=page.extract_text(), metadata=dict(file_name=filename, pdf_num=idx, page_num=i)))
    return FAISS.from_documents(list_of_documents, embeddings)

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

"""
分割列表utils函数
"""
def chunk_list(input_list, chunk_size=50):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

"""
获取视频title utils函数
"""
def get_title(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(url)
    return yt.title

def get_youtube_embedding(video_id_list):
    list_of_documents = []
    for video_id in video_id_list:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            if transcript.language != 'English (auto-generated)':
                continue
            transcript_list = transcript.translate('zh-Hans').fetch()
            chunked_lists = chunk_list(transcript_list, 50)
            for t in chunked_lists:
                text = "".join(obj['text'] for obj in t)
                time = t[0]['start']
                list_of_documents.append(Document(page_content=text, metadata=dict(video_name=get_title(video_id), start_time=time)))
    return FAISS.from_documents(list_of_documents, embeddings)


