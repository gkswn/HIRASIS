from flask import Flask,render_template
import model_list as ml
from flask import Flask,request,Response,jsonify,render_template


app=Flask(__name__)
#순번,요양기관번호,요양기관명,예측결과,예측확률,입력변수

@app.route("/")
def index():
    return render_template('menu_test.html',data_list=data_list)



if __name__ == "__main__":
    data_list=ml.test()
    print('here')
    print(data_list)
    app.run(host="127.0.0.1",port="8080")
    
    