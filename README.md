# Amazon Captcha Solver API
A Flask API based solution for tackling captcha when collecting data from Amazon.

This is a Flask API based solution to solve the captcha, by accepting the captcha image from POST request. The API then calls the captcha solving script and sends the solved captcha text in return.

## How to use : ##
1. Run the Flask API script -
```
python solve_api.py
```

2. To check the status of API, call the default method by accessing its IP -
```
your_api_ip_address:5000    # '5000' being the default port for Flask Server, which hosts the API.
```

3. To call the captcha solver function with 'requests' module and passing captcha image as file -
```
import requests

def captcha_uploader():
    # API URL with a call to function to solve captcha
    captcha_solver_api_url = 'your_api_ip_address:5000/solve'
    # opening the captcha image file as binary and putting it as value for key 'captcha'
    file = {'captcha': open('your_captcha_image_filepath','rb')}
    
    # Calling the API function as a 'POST' request with 'files' parameter
    response = requests.post(captcha_solver_api_url, files=file)
    print("Captcha file uploaded.")

    # Fetching the captcha text from API response.
    try:
        captcha_text = resp.json()['output']
    except:
        print("Response not in JSON format. Please check your API code.")
        captcha_text = "NA"
    
    return captcha_text
```


The goal is to solve the captcha images from Amazon. Sample captcha image can be seen below -

![a sample captcha image](https://github.com/HRN-Projects/captcha-solver/blob/main/test_captchas/Captcha_iwhygarbwz.jpg)

## How to contribute : ##
1. Please start with installing all the required packages from requirements file-
  ```
  pip install requirements.txt
  ```

2. Then to initially run the model on test_captchas, use following command -
  ```
  python solve_captchas_with_model.py
  ```


The API works fine but can be enhanced further according to use cases. The API's reponses would be solely dependent upon the training quality of the model file.
