import os, datetime, time
from flask import Flask, request, jsonify
from solve_captcha_with_model import CaptchaSolver

run_date = datetime.datetime.strptime("2021-01-05", "%Y-%m-%d")
today = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")

if today != run_date:
    print("Date mismatch!")
    exit()

app = Flask(__name__)
captchaSolver = CaptchaSolver()

app.config["DEBUG"] = True # turn off in prod

@app.route('/', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "Captcha solver service is up and running."


@app.route('/solve', methods=["POST"])
def solve_captcha():
    img = request.files['captcha']
    if img.filename != '':
        img.filename = 'test.jpg'
        time.sleep(2)
        img.save(img.filename)
        captcha_output = captchaSolver.solve()
    else:
        captcha_output = "Image file invalid! Please try again."
    return jsonify({"output":captcha_output})

if __name__ == '__main__':
    app.run(host="0.0.0.0")

