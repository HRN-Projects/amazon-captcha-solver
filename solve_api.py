import os, datetime, time
from flask import Flask, request, jsonify
from solve_captcha_with_model import CaptchaSolver

# Below line can be set to some path. Uncomment if needed.
# image_file_path = ""

app = Flask(__name__)
captchaSolver = CaptchaSolver()

app.config["DEBUG"] = True # turn off in prod

@app.route('/', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "Captcha solver service is up and running."


@app.route('/solve', methods=["POST"])
def solve_captcha():
	"""Calls the captcha solver function and return solved captcha text in response"""
    img = request.files['captcha']
    if img.filename != '':
        img.filename = 'test.jpg'
        img.save(os.path.join(image_file_path, img.filename))
        captcha_output = captchaSolver.solve()
    else:
        captcha_output = "Image file invalid! Please try again."

    return jsonify({"output":captcha_output})

app.run(host="0.0.0.0")