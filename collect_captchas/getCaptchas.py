import requests
from bs4 import BeautifulSoup

# Dummy URL to get captcha from amazon.in
# hit this URL as many times as needed
url = 'https://www.amazon.in/errors/validateCaptcha?amzn=YChRKC0P99j%2BngDKjEVBOQ%3D%3D&amzn-r=%2Fxyz%2Fproduct-reviews%2FB07PBS4ML5%2Fref%3Dcm_cr_arp_d_viewopt_srt%3Fie%3DUTF8%26reviewerType%3Dall_reviews%26sortBy%3Drecent%26pageNumber%3D1'

# input a number - Number of captcha files which needs to be collected
num = int(input("Enter number of captcha files to be fetched : "))

# Looping of given range of to hit above URL and fetch image from each hit
for i in range(num):
    r = requests.get(url)

    # Parse the page with BS4 html parser
    soup = BeautifulSoup(r.text, "html.parser")
    image = soup.find('img')
    image_url = image['src']

    # Split the image path stored on Amazon Server on basis of '/' in file path
    url_list = image_url.split('/')

    # Get the image, save it in same naming and file format from website
    # Saves the file on same level of this program. Change the path on line 26, if needed.
    r2 = requests.get(image_url, allow_redirects=True)
    open(url_list[-1], 'wb').write(r2.content)
    print('[INFO] ----- Saved file "{}"'.format(url_list[-1]))
