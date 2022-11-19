from flask import Flask,render_template
import model_list as ml
import model_content as ct
import model_content_right as cr
from flask import Flask,request,Response,jsonify,render_template
import pickle
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
app=Flask(__name__)
#순번,요양기관번호,요양기관명,예측결과,예측확률,입력변수
plt.style.use('default')
plt.rcParams['figure.figsize']=(4,2)
plt.rcParams['font.size']=8

font={'family':'GULIM','size':'10'}
@app.route("/")
def index():
    return render_template('main3.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/model_predict.html")
def model_predict():
    return render_template('model_predict.html')


#html -> model_start.js (성공)->app.py 데이터 ->model_start.js
@app.route('/item_request',methods=['POST'])
def item_query():
    #js에서 받은 값
    value1=request.form['year_name']
    value2=request.form['month_name']
    #년도와 month의 대한 list(순번,요양기관기호,요양기관명,예측결과,예측점수,총 청구 건수)
    #dflist를 html로 보내주어야함.
    print(value1,value2)
    
    data_list=ct.model_contnet(value1,value2)
    print(data_list)
    return data_list


#통계치 실행하는 버튼
@app.route('/model_result',methods=['POST'])
def model_result():
    #js에서 받은 값
    with open('content_list.pickle','rb') as f:
        all_list=pickle.load(f)
      
    print('startmodel_result')
    year_month_num=request.form['num_result']
    #통계치뽑는 파이썬 파일 넣어주기
    year=year_month_num[:4]
    month=year_month_num[4:6]
    show_num=year_month_num[6:]
    print(year,month,show_num)
    
    select=cr.right_result(year,month,show_num)

    print('select',select)
    return select




#@app.route("/model_predict_show.html")
#def model_show_html():
    #return render_template('model_predict_show.html',data_list=data_list)




if __name__ == "__main__":
    
    app.run(host="127.0.0.1",port="8080")
    
    