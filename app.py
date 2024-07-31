from flask import Flask, render_template, request
from PIL import Image, ImageOps 
import numpy as np
app = Flask(__name__)

def rgb_to_hex(rgb): 
    return '%02x%02x%02x' % rgb

#function to get primary color
def primary_color(file_path, code):
    my_image = Image.open(file_path).convert('RGB')
    img_size = my_image.size #giving 2-tuple (width, height), containing the horizontal and vertical size in pixels
    if img_size[0] >=1200 or img_size[1] >=1200: #Scaling Down the Image  to reduce the number of pixels, which makes the image easier and faster to analyze 
        my_image = ImageOps.scale(image=my_image, factor=0.6) #Larger Images: if the original size is 1200x800 pixels, it will be resized to 60% of its original size
    elif img_size[0] >=800 or img_size[1] >=800:
        my_image = ImageOps.scale(image=my_image, factor=0.5) #Moderately Large Images: resized to 50% of its original size
    elif img_size[0] >=600 or img_size[1] >=600:
        my_image = ImageOps.scale(image=my_image, factor=0.4) #Smaller Images: resized to 40% of its original size
    elif img_size[0] >=400 or img_size[1] >=400:
        my_image = ImageOps.scale(image=my_image, factor=0.2) #Smaller Images: resized to 20% of its original size
    my_image = ImageOps.posterize(image=my_image, bits=2) #Posterizing an image reduces the number of distinct colors used in the image by reducing the number of bits per color channel,helps to focus on primary colors

    # counting unique color iof the image by converting it to numpy array
    img_array = np.array(my_image)
    unique_colors = {}
    for row in img_array:
        for rgb in row:
            tuple_rgb = tuple(rgb)
            if tuple_rgb not in unique_colors:
                unique_colors[tuple_rgb] = 1
            else:
                unique_colors[tuple_rgb] += 1

    sorted_unique_colors = dict(sorted(unique_colors.items(), key = lambda x:x[1], reverse=True))
    values = list(sorted_unique_colors.keys())

    top_10 = values[0:10]

    if code == "hex":
        hex_list = []
        for key in top_10:
            hex = rgb_to_hex(key)
            hex_list.append(hex)
            return hex_list
        else:
            return top_10






@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        img = request.files["raw_image"]      #getting file from the form
        choice = request.form["color_code"]
        color = primary_color(img.stream, choice) #The file is not sent wholely over the internet, it is sent in chunks of data, and we read these chunks using this stream property.
        return render_template("base.html", color_list=color, color_code=choice)
    return render_template("base.html") # If the method is not POST, then simply render the frontend, if the method is POST, we pass our image file to a function that evaluates it. 

if __name__ == "__main__":
    app.run(debug = True)

#The items() method returns a view object. The view object contains the key-value pairs of the dictionary, as tuples in a list.