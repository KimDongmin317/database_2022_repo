from typing import Optional
from fastapi import APIRouter
import pymysql


import pandas as pd
import numpy as np
import os

from konlpy.tag import Okt
from collections import Counter
import re

from api import tf_idf_api

def select_db(sql, data_list):
    conn = pymysql.connect(user='kimdm', password='1q2w3e4r', host='db', db='database_2022', charset='utf8')

    cursor = conn.cursor()
    cursor.execute(sql, data_list)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    print("select success! result : {}".format(result))
    
    return result

def tuple_to_element(element):
    return element[0]
    
    
    
    
router = APIRouter(
    prefix="/api",
)



# 리뷰 get
@router.get("/get_review")
def get_review_with_class_professor(class_name: str, professor_name: str):
    query_params = [class_name, professor_name]
    sql = "SELECT * FROM review WHERE review.everytime_lecture_number = (SELECT everytime_info.everytime_lecture_number FROM everytime_info, univ_excel WHERE everytime_info.class_code_num = univ_excel.class_code_num AND univ_excel.class_name=%s AND univ_excel.professor_name=%s)"
    res = select_db(sql=sql, data_list=query_params)
    print(res)
    return res
    

# ML 결과 GET 
@router.get("/ML_result")
def tf_idf_with_review(class_name: str, professor_name: str):
    query_params = [class_name, professor_name]
    sql = "SELECT review FROM review WHERE review.everytime_lecture_number = (SELECT everytime_info.everytime_lecture_number FROM everytime_info, univ_excel WHERE everytime_info.class_code_num = univ_excel.class_code_num AND univ_excel.class_name=%s AND univ_excel.professor_name=%s)"
    res = list(map(tuple_to_element, list(select_db(sql=sql, data_list=query_params))))
    #####################
    # 리뷰 조회하고 해당 결과 바탕으로 ML 결과를 res 변수에 넣고 리턴
    res = {"res": list(tf_idf_api.tf_idf_api(res))}
    print("success {}".format(res))
    
    ####################
    return res