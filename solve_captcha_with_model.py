from tensorflow.keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
import tensorflow as tf
import os
import pathlib

class CaptchaSolver:
    def __init__(self):
        home_path = pathlib.Path(__file__).parent.absolute()
        self.MODEL_FILENAME = os.path.join(home_path, "amz_captcha_model.hdf5")
        self.MODEL_LABELS_FILENAME = os.path.join(home_path, "amz_captcha_model_labels.dat")
        # self.IMAGE_FILE = "/home/webspider/hrn/projects/amazon-captcha-solver-main/test.jpg"


    def solve(self, captcha_file):
        # Load up the model labels (so we can translate model predictions to actual letters)
        with open(self.MODEL_LABELS_FILENAME, "rb") as f:
            lb = pickle.load(f)

        tf.compat.v1.disable_eager_execution()

        # Load the trained neural network
        model = load_model(self.MODEL_FILENAME)

        try:
            # Load the image and convert it to grayscale
            image = cv2.imread(captcha_file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Add some extra padding around the image
            image = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

            # threshold the image (convert it to pure black and white)
            thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # find the contours (continuous blobs of pixels) the image
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        except Exception as e:
            return "Image recognition error. {}".format(str(e))

        # Hack for compatibility with different OpenCV versions
        contours = contours[0]

        letter_image_regions = []

        # Now we can loop through each of the four contours and extract the letter
        # inside of each one
        for contour in contours:
            # Get the rectangle that contains the contour
            (x, y, w, h) = cv2.boundingRect(contour)

            # Compare the width and height of the contour to detect letters that
            # are conjoined into one chunk
            if w / h > 1.25:
                # This contour is too wide to be a single letter!
                # Split it in half into two letter regions!
                half_width = int(w / 2)
                letter_image_regions.append((x, y, half_width, h))
                letter_image_regions.append((x + half_width, y, half_width, h))
            else:
                # This is a normal letter by itself
                letter_image_regions.append((x, y, w, h))

        # If we found more or less than 6 letters in the captcha, our letter extraction
        # didn't work correcly. Skip further processing and print output.
        if len(letter_image_regions) != 6:
            return "Couldn't solve the uploaded captcha file: bad length {}".format(str(len(letter_image_regions)))
        else:
            # Sort the detected letter images based on the x coordinate to make sure
            # we are processing them from left-to-right so we match the right image
            # with the right letter
            letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

            # Create an output image and a list to hold our predicted letters
            output = cv2.merge([image] * 3)
            predictions = []

            try:
                # loop over the letters
                for letter_bounding_box in letter_image_regions:
                    # Grab the coordinates of the letter in the image
                    x, y, w, h = letter_bounding_box

                    # Extract the letter from the original image with a 2-pixel margin around the edge
                    letter_image = image[y - 2:y + h + 2, x - 2:x + w + 2]

                    # Re-size the letter image to 20x20 pixels to match training data
                    letter_image = resize_to_fit(letter_image, 20, 20)

                    # Turn the single image into a 4d list of images to make Keras happy
                    letter_image = np.expand_dims(letter_image, axis=2)
                    letter_image = np.expand_dims(letter_image, axis=0)

                    # Ask the neural network to make a prediction
                    prediction = model.predict(letter_image)

                    # Convert the one-hot-encoded prediction back to a normal letter
                    letter = lb.inverse_transform(prediction)[0]
                    predictions.append(letter)

                    # draw the prediction on the output image
                    cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
                    cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
            except Exception as e:
                print("Exception in looping letter contours.")
                return "Image recognition error. {}".format(str(e))

            # Print the captcha's text
            captcha_text = "".join(predictions)
            return captcha_text