import datetime
import os
from curvy import builder
from flask import Flask, jsonify, abort
from flask import request

app = Flask(__name__)

@app.route("/curvy", methods = ['POST'] )
def main():
   json_input = request.get_json()

   print('Input: ' + json_input['securityKey'])
   print('Env: ' + os.environ.get('SECURITY_KEY'))

   if 'securityKey' not in json_input.keys() or json_input['securityKey'] != os.environ.get('SECURITY_KEY'):
      return abort(403)

   start_date = datetime.datetime.strptime(json_input['baselineDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
   forward_curve = json_input['forwardCurve']

   forwards = []
   for i in range(len(forward_curve)):
      forwards.append(forward_curve[i]['price'])  

   x, _, _, _ , y_smfc = builder.build_smfc_curve(forwards, start_date)

   ret = []
   for i in range(len(y_smfc)):
      ret.append({"day": x[i].strftime('%Y-%m-%dT%H:%M:%SZ'), "price": y_smfc[i]})

   return jsonify(ret)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)