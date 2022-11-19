def test(year,month):
    # 라이브러리 설정
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.svm import OneClassSVM

    #===========================================================
    # 파일 불러오기 (학습 데이터)
    #===========================================================
    path = "C:\\lab\\bigleader\\심평원\\web\\input\\"+year+"\\"+month #경로설정
    df_origin = pd.read_csv(path+'\\df.txt', sep=',',encoding='cp949') #학습데이터

    df = df_origin.drop(['병원기호','종별코드'],axis=1) #구분기호 제거


    #===========================================================
    # 학습데이터 정규화 (0~1사이 수)
    #===========================================================
    # 이상치를 더욱 띄워주어야 하기 때문에 minmaxscaler사용
    df1 = df
    minmax = MinMaxScaler()
    minmax.fit(df1)

    minmax_data = minmax.transform(df1)
    minmax_df = pd.DataFrame(minmax_data,columns = df1.columns)

    # 기존 학습 데이터에서 min과 max column별로 구하기
    min = list(df.min(axis=0))
    max = df.max(axis=0)
    list(max)
    df_minmax = pd.DataFrame({'min':min,'max':max})
    df_minmax = df_minmax.transpose() #행렬 변경 (학습데이터와 맞추기)

    #===========================================================
    # 데이터 비지도 이상치 탐지
    #===========================================================

    # nu =0.015는 상위 200개정도의 기관의 이상기준을 탐색 (기존 심평원의 기준에 부합)
    # nu =0.015는 상위 200개정도의 기관으로 테스트 하였을 때 가장 성능이 좋은것으로 판단. 추후에 변경 가능
    model1 = OneClassSVM(kernel='rbf',gamma=0.001,nu = 0.015)
    model1.fit(minmax_df)

    pred1 = model1.predict(minmax_df)   #예측
    pred2 = pd.DataFrame(pred1)         #데이터프레임으로 만들기
    df2 = pd.concat([df_origin,pred2],axis=1)          #원본dataframe에 이상여부 붙이기
    df2.rename(columns={0:'이상여부'},inplace=True) #이상여부 컬럼명 변경
    df3 = pd.concat([minmax_df,pred2],axis=1)          #정규화된 dataframe에 이상여부 붙이기
    df3 = pd.concat([df_origin['병원기호'],df3],axis=1)          #정규화된 dataframe에 이상여부 붙이기
    df3.rename(columns={0:'이상여부'},inplace=True)    #이상여부 컬럼명 변경



    # 분류기준 설정완료 ------------------------------------
    #------------------------------------------------------



    #===========================================================
    # 파일 불러오기 (예측 데이터)
    #===========================================================
    # 예측을 위한 통합 코드가 여기서 돌아가야함.


    #===============================================================================================================================
    # 입력데이터 불러오기
    #===============================================================================================================================
    #--------------100T 읽기---------------------------------------------------
    try : #encoding 에러 확인
        input_100T = pd.read_csv(path+'\\가_100.txt', sep=',',encoding='cp949')
    except :
        input_100T = pd.read_csv(path+'\\가_100.txt', sep=',',encoding='UTF8')
    #--------------200T 읽기---------------------------------------------------
    try : #encoding 에러 확인
        input_200T = pd.read_csv(path+'\\가_200.txt', sep=',',encoding='cp949')
    except :
        input_200T = pd.read_csv(path+'\\가_200.txt', sep=',',encoding='UTF8')
    #--------------300T 읽기---------------------------------------------------
    try : #encoding 에러 확인
        input_300T = pd.read_csv(path+'\\가_300.txt', sep=',',encoding='cp949')
    except :
        input_300T = pd.read_csv(path+'\\가_300.txt', sep=',',encoding='UTF8')
    #--------------400T 읽기---------------------------------------------------
    try : #encoding 에러 확인
        input_400T = pd.read_csv(path+'\\가_400.txt', sep=',',encoding='cp949')
    except :
        input_400T = pd.read_csv(path+'\\가_400.txt', sep=',',encoding='UTF8')

    #============================================
    # 필요변수만 선택
    #============================================
    # 100 - 병원기호, 병원종류코드
    input_100T = input_100T.loc[:,['YKIHO','RECU_CL_CD']]
    # 200 - 명세서번호,병원기호,입원여부,내원일수,청구총금액,기본진료소계금액,청구원내외래약제비금액,응급환자여부,주상병코드
    input_200T = input_200T.loc[:,['SPEC_ID','YKIHO','FOM_CD','VST_DDCNT','DMD_TOT_AMT','BSE_DIAG_STOT_AMT',\
                                    'DMD_IHSP_OPAT_DGMAMT_AMT','EMY_DIAG_YN','MSICK_SICK_SYM']]
    # 300 - 명세서번호, 진료금액, 진료명
    input_300T = input_300T.loc[:,['SPEC_ID','DIAG_AMT','DIV_CD_NM']]
    # 명세서번호
    input_400T = input_400T.loc[:,['SPEC_ID']]

    #============================================
    # 모든 테이블 명세서로 묶기
    #============================================

    # 각 변수의 통계치 구하기 위한 딕셔너리 만들기
    count_400dic = {}
    for i in range(len(input_400T)):
        id = input_400T.iloc[i]['SPEC_ID']
        if id not in count_400dic:
            count_400dic[id]=0
        count_400dic[id]+=1 #상병수 count

    count_300dic = {}
    for i in range(len(input_300T)):
        id = input_300T.iloc[i]['SPEC_ID']
        amt = input_300T.iloc[i]['DIAG_AMT']
        name = input_300T.iloc[i]['DIV_CD_NM']
        if id not in count_300dic:
            #[진료행위 수, 진료금액 합, 2부위행위 합]
            count_300dic[id]=[0,0,0]

        count_300dic[id][0]+=1 #진료행위 수 count
        count_300dic[id][1]+=amt #진료금액 합
        if "2부위" in name:
            count_300dic[id][2]+=1 #행위 2부위수 count

    #딕셔너리를 테이블로 만들기
    df_input_300T = pd.DataFrame(list(count_300dic.items()),columns=['SPEC_ID','LIST_300'])
    df_input_300T['COUNT_300']=0
    df_input_300T['진료당_진료금액_300']=0
    df_input_300T['2부위_300']=0
    df_input_400T = pd.DataFrame(list(count_400dic.items()),columns=['SPEC_ID','COUNT_400'])
    for i in range(len(df_input_300T)):
        df_input_300T.loc[i,['COUNT_300']] = df_input_300T.loc[i,['LIST_300']][0][0]
        df_input_300T.loc[i,['진료당_진료금액_300']] = df_input_300T.loc[i,['LIST_300']][0][1]/df_input_300T.loc[i,['LIST_300']][0][0]
        df_input_300T.loc[i,['2부위_300']] = df_input_300T.loc[i,['LIST_300']][0][2]
    df_input_300T = df_input_300T.drop(['LIST_300'],axis=1) #구분기호 제거



    # 200T로 통합
    input_200T = pd.merge(input_200T,df_input_300T,how='left',on='SPEC_ID')
    input_200T = pd.merge(input_200T,df_input_400T,how='left',on='SPEC_ID')

    #============================================
    # 경상환자만 남기기
    #============================================
    input_200T = input_200T.loc[:,:][(input_200T['MSICK_SICK_SYM'] == 'S060') | (input_200T['MSICK_SICK_SYM'] == 'S0600') | (input_200T['MSICK_SICK_SYM'] == 'S06090')
                   | (input_200T['MSICK_SICK_SYM'] == 'S134')  | (input_200T['MSICK_SICK_SYM'] == 'S136')  | (input_200T['MSICK_SICK_SYM'] == 'S335') 
                   | (input_200T['MSICK_SICK_SYM'] == 'S3350') | (input_200T['MSICK_SICK_SYM'] == 'S3351') | (input_200T['MSICK_SICK_SYM'] == 'S336') 
                   | (input_200T['MSICK_SICK_SYM'] == 'S337')  | (input_200T['MSICK_SICK_SYM'] == 'S100')  | (input_200T['MSICK_SICK_SYM'] == 'S300')
                   | (input_200T['MSICK_SICK_SYM'] == 'S400')  | (input_200T['MSICK_SICK_SYM'] == 'S602')  | (input_200T['MSICK_SICK_SYM'] == 'S434')]


    #============================================
    # 병원별로 묶기
    #============================================
    #--------------입원환자비율---------------------------------------------------
    for i in range(len(input_200T)+1):
        if input_200T.iloc[i]['FOM_CD'] == 12.0 :
            input_200T.loc[i,['FOM_CD']] = 1   
        else :
            input_200T.loc[i,['FOM_CD']] = 0
    input_200T.dropna(inplace=True)
    input_200T.reset_index(inplace=True)
    input_200T.drop(['index'],axis=1,inplace=True) #index 재정의로 인한 제거

    FOM_CD = input_200T.groupby(['YKIHO'])['FOM_CD'].agg(**{'입원환자비율':'mean'}).reset_index()

    #--------------평균내원일수---------------------------------------------------
    VST_DDCNT = input_200T.groupby(['YKIHO'])['VST_DDCNT'].agg(**{'평균내원일수':'mean'}).reset_index()

    #--------------청구총금액75%---------------------------------------------------
    DMD_TOT_AMT = input_200T.groupby(['YKIHO'])['DMD_TOT_AMT'].agg(**{'청구총금액75%':lambda x:x.quantile(0.75)}).reset_index()

    #--------------기본진료소계금액평균---------------------------------------------------
    BSE_DIAG_STOT_AMT = input_200T.groupby(['YKIHO'])['BSE_DIAG_STOT_AMT'].agg(**{'기본진료소계금액평균':'mean'}).reset_index()

    #--------------평균청구원내외래약제비금액---------------------------------------------------
    DMD_IHSP_OPAT_DGMAMT_AMT = input_200T.groupby(['YKIHO'])['DMD_IHSP_OPAT_DGMAMT_AMT'].agg(**{'평균청구원내외래약제비금액':'mean'}).reset_index()

    #--------------응급진료자비율---------------------------------------------------
    EMY_DIAG_YN = input_200T.groupby(['YKIHO'])['EMY_DIAG_YN'].agg(**{'응급진료자비율':'mean'}).reset_index()

    #--------------상병수---------------------------------------------------
    상병수 = input_200T.groupby(['YKIHO'])['COUNT_400'].agg(**{'상병수':'mean'}).reset_index()

    #--------------진료행위수---------------------------------------------------
    진료행위수 = input_200T.groupby(['YKIHO'])['COUNT_300'].agg(**{'진료행위수':'mean'}).reset_index()

    #--------------진료당진료금액---------------------------------------------------
    진료당진료금액 = input_200T.groupby(['YKIHO'])['진료당_진료금액_300'].agg(**{'진료당진료금액':'mean'}).reset_index()

    #--------------행위2부위평균---------------------------------------------------
    행위2부위평균 = input_200T.groupby(['YKIHO'])['2부위_300'].agg(**{'행위2부위평균':'mean'}).reset_index()

    #종별코드
    input_df = pd.merge(FOM_CD,VST_DDCNT,how='left',on='YKIHO')
    input_df = pd.merge(input_df,DMD_TOT_AMT,how='left',on='YKIHO')
    input_df = pd.merge(input_df,BSE_DIAG_STOT_AMT,how='left',on='YKIHO')
    input_df = pd.merge(input_df,DMD_IHSP_OPAT_DGMAMT_AMT,how='left',on='YKIHO')
    input_df = pd.merge(input_df,EMY_DIAG_YN,how='left',on='YKIHO')
    input_df = pd.merge(input_df,상병수,how='left',on='YKIHO')
    input_df = pd.merge(input_df,진료행위수,how='left',on='YKIHO')
    input_df = pd.merge(input_df,진료당진료금액,how='left',on='YKIHO')
    input_df = pd.merge(input_df,input_100T,how='left',on='YKIHO')
    input_df = pd.merge(input_df,행위2부위평균,how='left',on='YKIHO')
    input_df.rename(columns={'YKIHO':'병원기호'},inplace=True)
    input_df.rename(columns={'RECU_CL_CD':'종별코드'},inplace=True)
    #종별코드 재정리
    for i in range(len(input_df)):
        if input_df.iloc[i]['종별코드'] == 92 :
            input_df.loc[i,['종별코드']] = '한방병원'  
        else :
            input_df.loc[i,['종별코드']] = '한의원'

    #===========================================================
    # 데이터 정규화 (0~1사이 수) 예측
    #===========================================================
    # 새로운 프레임에 저장
    df_change = input_df
    df_change = df_change.drop(['병원기호','종별코드'],axis=1) #구분기호 제거
    print(df.columns)
    print(df_change.columns)
    for i in range(len(df_change)):
        for j in range(len(df.columns)):
            df_change.iloc[i][j] = (df_change.iloc[i][j]-df_minmax.iloc[0][j])/(df_minmax.iloc[1][j]-df_minmax.iloc[0][j])
    print(df_change)
    print("===================")
    #===========================================================
    # 이상여부 예측하기
    #===========================================================

    pred1 = model1.predict(df_change)   #예측
    pred2 = pd.DataFrame(pred1)         #데이터프레임으로 만들기
    df2_pred = pd.concat([input_df,pred2],axis=1)          #dataframe에 이상여부 붙이기
    df2_pred.rename(columns={0:'이상여부'},inplace=True) #이상여부 컬럼명 변경

    df3_pred = pd.concat([df_change,pred2],axis=1)          #정규화된 dataframe에 이상여부 붙이기
    df3_pred = pd.concat([input_df['병원기호'],df3_pred],axis=1)          #정규화된 dataframe에 이상여부 붙이기
    df3_pred.rename(columns={0:'이상여부'},inplace=True)    #이상여부 컬럼명 변경

    df3_pred['이상여부'].replace({'1':'이상기관','-1':'정상기관'},inplace=True)
    print("end")

    #===========================================================
    # 원본 업데이트 (다음 학습에 적용하기 위함)
    #===========================================================
    # print(df2.head())
    print(df2_pred)
    #===========================================================
    # 정규화 된것 내보내기 (이상항목 알려주기 위함)
    #===========================================================

    print(df3_pred)
    print('list',df3_pred.values.tolist())
    
    test={}
    for num,i in enumerate(df3_pred.values.tolist()):
        test[num]=i
        
    print(test)
        
    return test




