"""
    Created by Yash Sharma
"""

from flask import Flask,  render_template, jsonify, request
from werkzeug.utils import redirect
import util
import numpy as np

app = Flask(__name__, template_folder="../client/html", static_folder="../client/static")
app.config['UPLOAD_FOLDER'] ="upload"
app.secret_key = "Yash Sharma" 

@app.route('/')
def home():
    print("Home Page Accessed")
    return render_template("app.html")

@app.route('/home')
def home1():
    print("Home Page Accessed")
    return render_template("app.html")

@app.route('/service')
def service():
    res = request.args.get('res', None)
    formdata = request.args.get('formdata', None)
    return render_template("services.html", res=res, formdata=formdata)

@app.route('/dirt_detect', methods=['POST'])
def dirt_detect():
    data = request.files['file']
    res = util.dirt_detect(data)
    response = jsonify({
        'prediction' : res[0],
        'accuracy' : res[1]
    })
    response.headers.add('Access-Control-Allow-Origin','*')

    return response

@app.route('/predict_power', methods=['POST'])
def predict_power():
    if request.method=='POST':
        X_test = ['Latitude', 'Humidity', 'AmbientTemp', 'Wind.Speed',
                     'Visibility', 'Pressure', 'Cloud.Ceiling', 'Grissom',
                     'Camp Murray', 'Hill Weber', 'JDMT',
                     'Kahului', 'MNANG', 'Malmstrom',
                     'March AFB', 'Offutt', 'Peterson',
                     'Travis', 'USAFA','Fall','Spring',
                     'Summer', 'Winter', 'delta_hr', 'sine_mon',
                     'cos_mon', 'sine_hr', 'cos_hr']
        X_test[0] = float(request.form.get('latitude'))
        X_test[1] = float(request.form.get('humidity'))
        X_test[2] = float(request.form['amb_temp'])
        X_test[3] = float(request.form['wind speed'])
        X_test[4] = float(request.form['visibility'])
        X_test[5] = float(request.form['pressure'])
        X_test[6] = int(request.form['cloud ceiling'])

        for i in range(7,19):
            if request.form['location']==X_test[i]:
                X_test[i]=1
            else:
                X_test[i]=0
        
        for i in range(19,23):
            if request.form['season']==X_test[i]:
                X_test[i]=1
            else:
                X_test[i]=0

        X_test[23] = int(request.form['time'][:2])-10
        X_test[24] = int(np.sin((int(request.form['date'][5:7]) - 1)*np.pi/11))
        X_test[25] = int(np.cos((int(request.form['date'][5:7]) - 1)*np.pi/11))
        X_test[26] = int(np.cos((int(request.form['time'][:2]) - 1)*np.pi/11))
        X_test[27] = int(np.cos((int(request.form['time'][:2]) - 1)*np.pi/11))

        res = util.predict(np.array(X_test).reshape(1,-1))[0][0]
        formdata = request.form
        return render_template("services.html", res=str(res), formdata=formdata)


if __name__=="__main__":
    print("Starting Flask Server....")
    app.run(debug=True)