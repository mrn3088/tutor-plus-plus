import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from htmlTemplates import css, bot_template
from api import query

from model_inference import *
from utils import *


# input = "知乎，是一个中文互联网高质量问答社区和创作者聚集的原创内容平台，于2011年1月正式上线，以“让人们更好地分享知识、经验和见解，找到自己的解答”为品牌使命。知乎凭借认真、专业、友善的社区氛围、独特的产品机制以及结构化和易获得的优质内容，聚集了中文互联网科技、商业、影视、时尚、文化领域最具创造力的人群，已成为综合性、全品类、在诸多领域具有关键影响力的知识分享社区和创作者聚集的原创内容平台，建立起了以社区驱动的内容变现商业模式。 [1]知乎，2017年11月8日入选时代影响力·中国商业案例TOP30。 [2] 2019年10月21日，胡润研究院发布《2019胡润全球独角兽榜》，知乎排名第138位。 [3] 6月6日原有的“知识市场”业务升级为“知乎大学”。 [4] 7月，知乎完成新一轮融资，融资额接近3亿美元。 [5] 2019年8月12日，知乎宣布完成F轮融资，总额4.34亿美元。 [6]截至2020年12月，知乎上的总问题数超过4400万条，总回答数超过2.4亿条。在付费内容领域，知乎月活跃付费用户数已超过250万，总内容数超过300万，年访问人次超过30亿。 [7]知乎以问答业务为基础，经过近十年的发展，已经承载为综合性内容平台，覆盖“问答”社区、全新会员服务体系“盐选会员”、机构号、热榜等一系列产品和服务，并建立了包括图文、音频、视频在内的多元媒介形式。 [8]2022年4月22日，知乎在港交所实现双重上市 [45] 。"
input = ""


def load_models():
    embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
    db_videos_coarse = FAISS.load_local("./embeddings/faiss_youtube_embedding", embeddings)
    db_books_coarse = FAISS.load_local("./embeddings/faiss_pdf_embedding", embeddings)
    db_videos = FAISS.load_local("./embeddings/faiss_youtube_embedding_paging", embeddings)
    db_books = FAISS.load_local("./embeddings/faiss_pdf_embedding_paging", embeddings)
    return embeddings, db_videos_coarse, db_books_coarse, db_videos, db_books

def handle_userinput(user_question):
    # Use question_utils to format user input
    print("***question: ", user_question)

    # Use model_inference to perform inference
    response = query(db_videos_coarse=st.session_state.db_videos_coarse, db_books_coarse=st.session_state.db_books_coarse, db_videos=st.session_state.db_videos, db_books=st.session_state.db_books, question=user_question)
    print("***response: ", response)
    st.session_state.chat_history = response

    # Assuming response is a single string message
    st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Justice: What's The Right Thing To Do?",
                       page_icon=":books:")

    # Check if the models are already loaded in session state
    if "embeddings" not in st.session_state:
        with st.spinner("加载模型中..."):
            st.session_state.embeddings, st.session_state.db_videos_coarse, st.session_state.db_books_coarse, st.session_state.db_videos, st.session_state.db_books = load_models()
    # Otherwise, the models are already in session state and we don't need to reload them
    st.markdown(css, unsafe_allow_html=True)

    # if "conversation" not in st.session_state:
    #     st.session_state.conversation = None
    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = None

    st.header("Justice: What's The Right Thing To Do? :books:")
    st.subheader("Powered by :blue[Tutor++] :school:", divider='rainbow')
    st.caption(""""Justice: What's the Right Thing to Do?" is a book written by Michael J. Sandel, a prominent political philosopher and professor at Harvard University.
    The book explores various ethical and philosophical questions related to justice and morality. Sandel examines a wide range of topics, including distributive justice,
    individual rights, the role of government, and the moral dilemmas that arise in everyday life. Below is the course video link: [Course Link](https://www.youtube.com/playlist?list=PL30C13C91CFFEFEA6)""")
    
    user_question = st.text_input(
        "Ask a question about the book and its related course:")
    if st.button("Submit") and (user_question is not None):
        with st.spinner("处理中..."):
            handle_userinput(user_question)

if __name__ == '__main__':
    main()

