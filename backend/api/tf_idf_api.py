import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer

from konlpy.tag import Okt
from collections import Counter
import re
import warnings

warnings.filterwarnings('ignore')

stopwords = pd.read_csv("./api/korean_stopwords.txt").values.tolist()
#나중에 우리 데이터만의 특화된 불용어 있으면 추가하기


def text_cleaning(review, stopwords=stopwords): #데이터 정제
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')
    result = hangul.sub('', review)
    okt = Okt()  # 형태소 추출
    nouns = okt.nouns(result)
    nouns = [x for x in nouns if len(x) > 1]  # 한글자 키워드 제거
    nouns = [x for x in nouns if x not in stopwords]  # 불용어 제거
    nouns = ' '.join(nouns)
    return nouns

def tf_idf_api(review):
    tfidf_vectorizer = TfidfVectorizer()
    review = list(map(lambda x:text_cleaning(review=x), review))
    response = tfidf_vectorizer.fit_transform(review)
    
    feature_array = np.array(tfidf_vectorizer.get_feature_names()) #list of features
    
    sorted_features = np.argsort(response.toarray()).flatten()[:-1] #index of highest valued features

    #printing top 3 weighted features
    n = 10
    top_n = feature_array[sorted_features][:n]
    print(top_n)
    
    return top_n