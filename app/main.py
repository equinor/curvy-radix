import os
import datetime
import statistics
from curvy import builder
from flask import Flask, jsonify, abort, request
from curvy import axis

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False   

@app.route("/curvy", methods = ['POST'] )
def main():
   json_input = request.get_json()

   # securityKey in json must match SECURITY_KEY in environment (configured as secret in Omnia Radix)
   if 'securityKey' not in json_input.keys() or json_input['securityKey'] != os.environ.get('SECURITY_KEY'):
      return abort(403)

   baseline_day = datetime.datetime.strptime(json_input['baselineDay'], '%Y-%m-%dT%H:%M:%S.%fZ')
   forward_curves = json_input['forwardCurves']

   ret = []
   for forward_curve in forward_curves:
      ret.append ( smooth_forward_curve(baseline_day, forward_curve) )

   return jsonify(ret)

def smooth_forward_curve(baseline_day, forward_curve):
   # dr - Array of array, each array containing dates in period.
   # pr - Array of array, each array containing the forward price (same price) for each day of the period.
   # y_smfc - Array of array, each array containing the smoothed forward price for each day of the period.
   _, _, dr, pr, y_smfc = builder.build_smfc_curve(forward_curve['curve'], baseline_day, False)
   curve = []
   period_average = []
   market = forward_curve['market']
   for periodIndex in range(len(y_smfc)):
      
      # Calculate and return average price for each period used for sanity check.
      forward_price = pr[periodIndex][0]
      average_price = statistics.mean(y_smfc[periodIndex])
      period_average.append(
         { 
            "firstDay" : dr[periodIndex][0].strftime('%Y-%m-%dT%H:%M:%SZ'),
            "lastDay" : dr[periodIndex][-1].strftime('%Y-%m-%dT%H:%M:%SZ'),
            "forwardPrice" : forward_price,
            "averagePrice" : average_price,
            "difference" : forward_price - average_price
         })

      # Create actual smoothen forward curve.
      for dayWithinPeriod in range(len(y_smfc[periodIndex])):
         curve.append(
            {
               "day": dr[periodIndex][dayWithinPeriod].strftime('%Y-%m-%dT%H:%M:%SZ'), 
               "price": y_smfc[periodIndex][dayWithinPeriod]
            })

   return { "market": market, "curve": curve, "periodAverage": period_average}

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
