from flask import Flask,request,jsonify
import numpy as np
from scipy.signal import find_peaks
import pandas as pd


app = Flask(__name__)


@app.route('/data_process',methods=['GET'])
def data_process():
    dict1={}
    if '[' and ']' and "," in request.args['C1 raw']:
        input_control=request.args['C1 raw'].strip('[').strip(']').split(',')
        #print(input_control)
        input_test=request.args['T1 raw'].strip('[').strip(']').split(',')
    elif ',' in request.args['C1 raw']:
        input_control=request.args['C1 raw'].split(',')
        print(input_control)
        input_test=request.args['T1 raw'].split(',')

    elif '\n' in  request.args['C1 raw']:
        input_control=request.args['C1 raw'].split('\n')
        input_control=input_control[0:-2]
        #print(input_control)
        input_test=request.args['T1 raw'].split('\n')
        input_test = input_test[0:-2]

    else:
        input_control=request.args['C1 raw'].split(' ')
        #print(input_control)
        input_test=request.args['T1 raw'].split(' ')


    peaks1, _ = find_peaks(input_control, prominence=1,width=15)
    peaks2, _ = find_peaks(input_test, prominence=1,width=15)
    if len(peaks1)!=0 or len(peaks2)!=0:
        print('Peak1: {} Peak2: {}'.format(peaks1, peaks2))
        peak_diff = float(input_control[peaks1[0]]) - float(input_test[peaks2[0]])
        percentage_change = (peak_diff) / float(input_control[peaks1[0]]) * 100
        if percentage_change < 19:
            result = 'Negative'
        elif percentage_change >= 19:
            result = 'Positive'

        dict1['Result']=result
        dict1['Peak C1 raw index']=str(peaks1[0])
        dict1['Peak T1 raw index']=str(peaks2[0])
        dict1['Peak C1 raw']=str(input_control[peaks1[0]])
        dict1['Peak T1 raw']=str(input_test[peaks2[0]])
        dict1['Peak Difference']=str(peak_diff)
        dict1['Percentage Change']=str(percentage_change)
        return jsonify(dict1)



    else:

        dict1['Result']='Inconclusive'
        dict1['Peak C1 raw index']='0'
        dict1['Peak T1 raw index']='0'
        dict1['Peak C1 raw']='0'
        dict1['Peak T1 raw']='0'
        dict1['Peak Difference']='0'
        dict1['Percentage Change']='0'
        return jsonify(dict1)








if __name__ == '__main__':
    app.run(debug=True)
#http://127.0.0.1:5000/data_process?control=[123456]&test=[546789]