# library
import pandas as pd
import pymysql
from konlpy.tag import Okt
import re

def insert_db(sql, data_list):
    conn = pymysql.connect(user='kimdm', password='1q2w3e4r', host='db', db='database_2022', charset='utf8')

    cursor = conn.cursor()
    cursor.executemany(sql, data_list)
    conn.commit()
    conn.close()
    print("insert finish : {}".format(sql))
    
#전처리 함수 만들기
def preprocessing(review, okt, remove_stopwords = False, stop_words =[]):
  #함수인자설명
  # review: 전처리할 텍스트
  # okt: okt객체를 반복적으로 생성하지 않고 미리 생성 후 인자로 받음
  # remove_stopword: 불용어를 제거할지 여부 선택. 기본값 False
  # stop_words: 불용어 사전은 사용자가 직접 입력, 기본값 빈 리스트

  # 1. 한글 및 공백 제외한 문자 모두 제거
  review_text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]','',review)
  
  #2. okt 객체를 활용하여 형태소 단어로 나눔
  word_review = okt.morphs(review_text,stem=True)

  if remove_stopwords:
    #3. 불용어 제거(선택)
    word_review = [token for token in word_review if not token in stop_words]
  return word_review

if __name__=="__main__":
    
    # univ excel
    univ_excel = pd.read_excel("./data/preprocessed_univ_excel.xlsx", index_col=0)
    univ_excel['class_code_num'] = univ_excel['class_code_num'].apply(str)
    univ_excel = univ_excel.dropna(axis=0)
    univ_excel = univ_excel.values.tolist()


    insert_sql1 = "INSERT INTO univ_excel (`class_code_num`, `class_name`, `professor_name`) VALUES (%s, %s, %s)"
    insert_db(sql=insert_sql1, data_list=univ_excel)
    
    # everytime_info
    everytime_info = pd.read_excel("./data/everytime_lecture_number.xlsx")
    everytime_info['everytime_lecture_number'] = everytime_info['everytime_lecture_number'].apply(str)
    everytime_info['class_code_num'] = everytime_info['class_code_num'].apply(str)
    everytime_info = everytime_info.drop_duplicates(['everytime_lecture_number'])
    everytime_info = everytime_info.values.tolist()
    
    insert_sql2 = "INSERT INTO everytime_info (`everytime_lecture_number`, `class_code_num`) VALUES (%s, %s)"
    insert_db(sql=insert_sql2, data_list=everytime_info)
    
    # review
    
    stop_words = ['은','는','이','가','하','아','것','들','의','있','되','수','보','주','등','한', '를', '에는', '에', '도']
    okt = Okt()
    
    review = pd.read_excel("./data/review_temp.xlsx", index_col=0)
    review["lecture_number"] = review["lecture_number"].apply(str)
    review["lecture_review"] = review["lecture_review"].apply(lambda x: preprocessing(review=x, okt=okt, remove_stopwords=True, stop_words=stop_words))
    review['lecture_review'] = review["lecture_review"].apply(lambda x: ' '.join(s for s in x))
    review = review.values.tolist()
    
    insert_sql3 = "INSERT INTO review (`id`, `everytime_lecture_number`, `review`, `star`) VALUES (%s, %s, %s, %s)"
    insert_db(sql=insert_sql3, data_list=review)
    