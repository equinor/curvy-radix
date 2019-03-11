import datetime
import json
from curvy import builder
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route("/curvy", methods = ['POST'] )
def curvy_radix():

   input = request.get_json()

   start_date = datetime.datetime.strptime(input['baselineDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
   forward_curve = input['forwardCurve']

   forwards = []
   for i in range(len(forward_curve)):

      forwards.append(forward_curve[i]['price'])  

   x, y, dr, pr, y_smfc = builder.build_smfc_curve(forwards, start_date)

   ret = []
   for i in range(len(y_smfc)):
      ret.append({"day": x[i].strftime('%Y-%m-%dT%H:%M:%SZ'), "price": y_smfc[i]})

   return jsonify(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)