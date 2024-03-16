import io
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import re
import base64
from PIL import Image
from skimage.io import imread, imsave
from inpainter import Inpainter
import math
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/apply_mask', methods=['POST'])
# def apply_mask():
#     data = request.get_json()
#     points = np.array(data['points'])
#     image_data = data['image_data']
#     og_img=data['original_image_data']
    
#     # Extract base64 image data
#     image_data = re.sub('^data:image/.+;base64,', '', image_data)
#     image_data = image_data.encode()
#     image_data = np.frombuffer(base64.decodebytes(image_data), np.uint8)
#     uploaded_image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

#     og_img = re.sub('^data:image/.+;base64,', '', og_img)
#     og_img = og_img.encode()
#     og_img = np.frombuffer(base64.decodebytes(og_img), np.uint8)
#     ogimg = cv2.imdecode(og_img, cv2.IMREAD_COLOR)
    
#     # Create an empty mask
#     mask = np.zeros_like(uploaded_image)
#     print(uploaded_image.shape)

#     # Apply the mask using the provided points
#     print(len(points))
#     cv2.fillPoly(mask, [points], color=(255, 255, 255))

#     # To Set the masked region to white
#     # masked_region = cv2.bitwise_and(mask, (255, 255, 255))

#     # masked_image = cv2.bitwise_and(uploaded_image, mask)

#     # Save the masked image
#     # gray_uploaded_image = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite('static/mask.jpg', mask)
#     cv2.imwrite('static/image.jpg', ogimg)

#     # Read the uploaded image
#     image = imread('static/image.jpg')
#     mask = imread('static/mask.jpg', as_gray=True)

#     # Inpainting parameters
#     height, width = image.shape[:2]
#     patch_size =9 # Set your default patch size here
#     print(patch_size)
#     output_image = Inpainter(image, mask, patch_size=patch_size).inpaint()
#     # Save the inpainted image to a BytesIO object
#     imsave('static/output.jpg', output_image, quality=100)
#     with open('static/output.jpg', 'rb') as f:
#         processed_image_data = base64.b64encode(f.read()).decode()

#     print("Length of processed image data:", len(processed_image_data))  # Add this line for debugging

#     return jsonify({'processed_image_data': processed_image_data})

# if __name__ == '__main__':
#     app.run(debug=True)


@app.route('/apply_mask', methods=['POST'])
def apply_mask():
    data = request.get_json()
    points = np.array(data['points'])
    image_data = data['image_data']
    og_img = data['original_image_data']
    
    # Extract base64 image data
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_data = image_data.encode()
    image_data = np.frombuffer(base64.decodebytes(image_data), np.uint8)
    uploaded_image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    og_img = re.sub('^data:image/.+;base64,', '', og_img)
    og_img = og_img.encode()
    og_img = np.frombuffer(base64.decodebytes(og_img), np.uint8)
    ogimg = cv2.imdecode(og_img, cv2.IMREAD_COLOR)
    
    # Create an empty mask
    mask = np.zeros_like(uploaded_image)

    # Convert points to the format expected by cv2.fillPoly
    points = points.reshape((-1, 1, 2)).astype(np.int32)

    # Apply the mask using the provided points
    cv2.fillPoly(mask, [points], color=(255, 255, 255))

    # Save the masked image
    cv2.imwrite('static/mask.jpg', mask)
    cv2.imwrite('static/image.jpg', ogimg)

    # Read the uploaded image
    image = imread('static/image.jpg')
    mask = imread('static/mask.jpg', as_gray=True)

    # Inpainting parameters
    height, width = image.shape[:2]
    patch_size = 9  # Set your default patch size here
    output_image = Inpainter(image, mask, patch_size=patch_size).inpaint()

    # Save the inpainted image to a BytesIO object
    imsave('static/output.jpg', output_image, quality=100)
    with open('static/output.jpg', 'rb') as f:
        processed_image_data = base64.b64encode(f.read()).decode()

    return jsonify({'processed_image_data': processed_image_data})

if __name__ == '__main__':
    app.run(debug=True)
