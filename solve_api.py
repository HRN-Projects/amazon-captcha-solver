import os, datetime, time, requests, tempfile, uuid
from flask import Flask, request, jsonify
from solve_captcha_with_model import CaptchaSolver

image_file_path = tempfile.gettempdir()

#run_date = datetime.datetime.strptime("2021-01-05", "%Y-%m-%d")
#today = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")

#if today != run_date:
#    print("Date mismatch!")
#    exit()

app = Flask(__name__)
captchaSolver = CaptchaSolver()

app.config["DEBUG"] = True
if (os.environ.get("PYTHON_ENV") == "production" or os.environ.get("PYTHON_ENV") == "staging"):
    app.config["DEBUG"] = False

@app.route('/', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "Captcha solver service is up and running."


@app.route('/solve', methods=["POST"])
def solve_captcha():
    img = request.files['captcha']
    if img.filename != '':
        captcha_file = os.path.join(image_file_path, str(uuid.uuid4()))
        time.sleep(2)
        img.save(captcha_file)
        captcha_output = captchaSolver.solve(captcha_file)
        os.unlink(captcha_file)
    else:
        captcha_output = "Image file invalid! Please try again."
    return jsonify({"output":captcha_output})

@app.route('/solveurl', methods=["GET"])
def solve_url():
    image_url = request.args.get('url', '')
    captcha_file = os.path.join(image_file_path, str(uuid.uuid4()))
    if image_url != '':
        try:
            response = requests.get(image_url, allow_redirects=True)
            print(str(response.headers['content-type']))
            open(captcha_file, "wb").write(response.content)
            captcha_output = captchaSolver.solve(captcha_file)
        except Exception as e:
            captcha_output = "Error retrieving captcha image: {}".format(str(e))
        finally:
            os.unlink(captcha_file)
    else:
        captcha_output = "Image URL invalid! Please try again."
    return jsonify({"output": captcha_output})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
