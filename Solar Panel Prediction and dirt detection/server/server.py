"""
    Created by Yash Sharma
"""

from flask import Flask,  render_template, jsonify, request
import util

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
    return render_template("services.html")

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

if __name__=="__main__":
    print("Starting Flask Server....")
    app.run(debug=True)