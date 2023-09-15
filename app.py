import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import requests
import json
import hashlib
import time

from model_inference import *
from utils import *


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


# def handle_userinput(user_question):
#     response = st.session_state.conversation({'question': user_question})
#     st.session_state.chat_history = response['chat_history']

#     for i, message in enumerate(st.session_state.chat_history):
#         if i % 2 == 0:
#             st.write(user_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)
#         else:
#             st.write(bot_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)


# input = "知乎，是一个中文互联网高质量问答社区和创作者聚集的原创内容平台，于2011年1月正式上线，以“让人们更好地分享知识、经验和见解，找到自己的解答”为品牌使命。知乎凭借认真、专业、友善的社区氛围、独特的产品机制以及结构化和易获得的优质内容，聚集了中文互联网科技、商业、影视、时尚、文化领域最具创造力的人群，已成为综合性、全品类、在诸多领域具有关键影响力的知识分享社区和创作者聚集的原创内容平台，建立起了以社区驱动的内容变现商业模式。 [1]知乎，2017年11月8日入选时代影响力·中国商业案例TOP30。 [2] 2019年10月21日，胡润研究院发布《2019胡润全球独角兽榜》，知乎排名第138位。 [3] 6月6日原有的“知识市场”业务升级为“知乎大学”。 [4] 7月，知乎完成新一轮融资，融资额接近3亿美元。 [5] 2019年8月12日，知乎宣布完成F轮融资，总额4.34亿美元。 [6]截至2020年12月，知乎上的总问题数超过4400万条，总回答数超过2.4亿条。在付费内容领域，知乎月活跃付费用户数已超过250万，总内容数超过300万，年访问人次超过30亿。 [7]知乎以问答业务为基础，经过近十年的发展，已经承载为综合性内容平台，覆盖“问答”社区、全新会员服务体系“盐选会员”、机构号、热榜等一系列产品和服务，并建立了包括图文、音频、视频在内的多元媒介形式。 [8]2022年4月22日，知乎在港交所实现双重上市 [45] 。"
input = ""


def handle_userinput(user_question):
    # Use question_utils to format user input
    input_data = question_utils(input, user_question)

    # Use model_inference to perform inference
    response = model_inference(input_data)

    st.session_state.chat_history = response

    # Assuming response is a single string message
    st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Justice: What's The Right Thing To Do?",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Justice: What's The Right Thing To Do? :books:")
    st.subheader("Powered by Tutor++")
    user_question = st.text_input(
        "Ask a question about your enrolled courses:")
    if user_question:
        handle_userinput(user_question)

    # with st.sidebar:
    #     st.subheader("Your documents")
    #     pdf_docs = st.file_uploader(
    #         "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    #     if st.button("Process"):
    #         with st.spinner("Processing"):
    #             # get pdf text
    #             raw_text = get_pdf_text(pdf_docs)

    #             # get the text chunks
    #             text_chunks = get_text_chunks(raw_text)

    #             # create vector store
    #             vectorstore = get_vectorstore(text_chunks)

    #             # create conversation chain
    #             st.session_state.conversation = get_conversation_chain(
    #                 vectorstore)


if __name__ == '__main__':
    main()
