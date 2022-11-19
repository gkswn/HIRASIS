from flask import Flask,request,Response,jsonify,render_template

app=Flask(__name__)
app.debug=True

import json


@app.route('/')
def index():
    return render_template('index_html')

@app.route('/search')
def item_search():
    return render_template('serch.html')

@app.route('/item_request',methods=['POST'])
def item_query():
    value1=request.form['item_id']
    item_sql='select * from student where id='+value1+''
    curs.execute(item_sql)
    row_headers=[x[0] for x in curs.desciption]
    rows=curs.fetchall()
    json_data=[]
    for result in rows:
        json_data.append(dict(zip(row_header,result)))
    json_return = json.dumps(json_data[0])
    return jsonify(json_return)

