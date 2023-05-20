from flask import Flask, render_template, request, jsonify
from SRT import SRT
import time
app = Flask(__name__)

@app.route("/") 	
def hello():			
    return render_template('index.html')

@app.route("/userData",methods=['POST'])
def userData():
    global srt
    param = request.get_json()
    srt = SRT(param['memberNumber'] , param['memberPassword'])
    return { "message" : f"{srt}" };

@app.route('/postUserData',methods=['POST'])
def postUserData():
    global trains
    param = request.get_json()
    depRe = param['depRe'] # 출발
    arrRe = param['arrRe'] # 도착
    dateRe = param['dateRe'] # 날짜 (yyyymmdd)
    timeRe = param['timeRe'] 
    trains = srt.search_train(depRe, arrRe, dateRe, timeRe, available_only=False)
    return f"{trains}"

@app.route('/goWhile',methods=["POST"])
def routing():
    param = request.get_json()
    reservation = srt.reserve(trains[param['idx']])
    return f"{reservation}"

@app.errorhandler(500)
def errorHandler_500(err):
    return f"{err}"

if __name__ == "__main__": 	#5
    app.run()