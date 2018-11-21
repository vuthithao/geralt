# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:22:00 2018

@author: Mr.Minh
"""
from flask import Flask, jsonify
from flask import request
import logging
import json
import service
import graypy
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
SERVICE_NAME = "Magico"
MAX_DOCUMENT = 20

@app.errorhandler(404)
def not_found(error):
    response = jsonify({'message': error.description,"status_code" : 404})
    response.status_code = 404
    response.status = 'error.Bad Request'
    return response,400

@app.errorhandler(500)
def server_error(error):
#    push_notify_to_slack('[{}]Date: {}, Error: {}'.format(SERVICE_NAME,str(datetime.datetime.now()),str(error)))
    if request.method == "POST":
        dataDict = json.loads(request.data)
        aid  = dataDict.get('content_id', None) 
        uid  = dataDict.get('user_id', None) 
        pid  = dataDict.get('place_id', None) 
    else:
        aid = request.args.get('content_id')
        uid = request.args.get('user_id')
        pid = request.args.get('place_id')
    log_data = {
                "content_id" : aid,
            }
    if uid is not None:
        log_data["user_id"] = uid
    if pid is not None:
        log_data["place_id"] = pid
        
    response = jsonify({'message': str(error),"status_code" : 500})
    response.status_code = 500
    response.status = 'Server error!'
    if service.NOT_TRAINED_CODE in str(error):
        app.logger.warn({"status" : "not trained","input" : log_data, "message" : str(error)})
    else:
        app.logger.error({"status" : "fail","input" : log_data, "message" : str(error)})
    return response,500


@app.route('/recommend', methods=['POST','GET'])
def recommendation():
    if request.method == "POST":
        dataDict = json.loads(request.data)
        aid  = dataDict.get('content_id', None) 
        uid  = dataDict.get('user_id', None) 
        pid  = dataDict.get('place_id', None) 
    else:
        aid = request.args.get('content_id')
        uid = request.args.get('user_id')
        pid = request.args.get('place_id')
    log_data = {
                "id" : aid,
            }
    if uid is not None:
        log_data["user_id"] = uid
    if pid is not None:
        log_data["place_id"] = pid
    y_pred = service.query(aid)
    app.logger.info({"status": "OK", "input" : log_data,"output" : y_pred})
    response = jsonify({"result" : y_pred,"status_code" : 200})
    response.status_code = 200
    response.status = 'OK'
    return response,200

if __name__ == "__main__":
    handler = graypy.GELFHandler(service.GRAY_LOG_URL, 5555)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',port='1408')
#    app.run()