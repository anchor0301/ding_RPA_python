# -*- coding: utf-8 -*-
"""
Created on Fri May 26 23:09:23 2023

@author: tlrtl
"""

from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/sensor', methods=['GET'])
def get_sensor_value():

    return jsonify({'sensor_value': "1"})


@app.route('/null', methods=['GET'])
def get_null_value():
    return jsonify({'sensor_value': "0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020)