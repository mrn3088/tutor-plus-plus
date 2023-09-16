from utils import *

def question_postprocessing(model_output, question, metadata_books, metadata_videos, score_books, score_videos):
    
    video_start_time = metadata_videos['start_time']
    start_time_min, start_time_second = sec_to_min(video_start_time)
    
    output_string = (
        "\n\n### 模型回答: \n"
        "> {}\n\n"
        "#### 书籍索引:\n"
        "- [查看书籍]({})\n"
        "- 索引文件名: {}\n"
        "- 索引页数: {}\n"
        "#### 视频索引:\n"
        "- [观看视频](https://www.youtube.com/watch?v={}&t={})\n"
        "- 索引视频名: {}\n"
        "- 索引视频时间戳: {} min {} sec\n"
    ).format(
        model_output, 
        'amazon.com',
        metadata_books['file_name'], 
        metadata_books['page_num'], 
        metadata_videos['video_id'], 
        str(int(float(str(metadata_videos['start_time'])))), 
        metadata_videos['video_name'], 
        start_time_min, 
        start_time_second
    )
                    
    return output_string
