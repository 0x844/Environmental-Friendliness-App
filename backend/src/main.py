from flask import request, jsonify, render_template, flash, Response
from config import app, db
from models import itemInfo
import barcode

app.secret_key = "00000000000000"

@app.route("/main", methods = ["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/camera", methods = ["POST","GET"])
def camera():
    return render_template("camera.html")

@app.route("/showScore", methods = ["POST","GET"])
def showScore():
    
    average = barcode.getData()
    productName = barcode.productNameAndDesc[0]
    imageLink = barcode.productImageLink
    
    return render_template("score.html", score = average, productName = productName,\
                           imageLink = imageLink)

@app.route("/open_cam", methods = ["POST","GET"])
def open_cam():
    barcode.startCam()
    return showScore()
     
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug = True, host = '192.168.1.81')