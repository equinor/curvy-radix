import datetime
import json
from curvy import builder
from flask import Flask, jsonify
from flask import request


app = Flask(__name__)

#   start_date = datetime.datetime.now()
# forward_prices = [3, 4, 6, 5, 7, 8, 6, 4, 5, 6]
#   x, y, dr, pr, y_smfc = builder.build_smfc_curve(forward_prices, start_date)
   # x, y, dr, pr, y_smfc = builder.build_smfc_curve(forward_prices, start_date)
# forward_prices = [3, 4, 6, 5, 7, 8, 6, 4, 5, 6]

@app.route("/curvy", methods = ['POST'] )
def hello():
   start_date = datetime.datetime.now()

   input = request.get_json()

   forwards = []
   for i in range(len(input)):
      json_dict = input[i]
      forwards.append(json_dict['price'])  

   x, y, dr, pr, y_smfc = builder.build_smfc_curve(forwards, start_date)

   ret = []
   for i in range(len(y_smfc)):
      ret.append({"day": x[i].strftime('%Y-%m-%dT%H:%M:%SZ'), "price": y_smfc[i]})

   return jsonify(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)