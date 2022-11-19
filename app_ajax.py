from flask import Flask,render_template

from flask import Flask,request,Response,jsonify,render_template


app=Flask(__name__)
#순번,요양기관번호,요양기관명,예측결과,예측확률,입력변수

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def item_search():
    return render_template('search.html')

@app.route('/item_request',methods=['POST'])
def item_query():
    #js에서 받은 값
    value1=request.form['item_id']
    test='hello_world'
    print('here')
    return test




if __name__ == "__main__":
    app.run(host="127.0.0.1",port="8080")
    
    