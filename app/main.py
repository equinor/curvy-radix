import datetime
import os
from curvy import builder
from flask import Flask, jsonify, abort
from flask import request

app = Flask(__name__)

@app.route("/curvy", methods = ['POST'] )
def main():
   json_input = request.get_json()

   if 'securityKey' not in json_input.keys() or json_input['securityKey'] != os.environ.get('SECURITY_KEY'):
      return abort(403)

   baseline_day = datetime.datetime.strptime(json_input['baselineDay'], '%Y-%m-%dT%H:%M:%S.%fZ')
   forward_curves = json_input['forwardCurves']

   ret = []
   for forward_curve in forward_curves:
      ret.append ( smooth_forward_curve(baseline_day, forward_curve) )

   return jsonify(ret)

def smooth_forward_curve(baseline_day, forward_curve):
   x, _, _, _ , y_smfc = builder.build_smfc_curve(forward_curve['curve'], baseline_day)
   curve = []
   market = forward_curve['market']
   for i in range(len(y_smfc)):
      curve.append({"day": x[i].strftime('%Y-%m-%dT%H:%M:%SZ'), "price": y_smfc[i]})
   return { "market": market, "curve": curve}

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)