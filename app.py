from flask import Flask, render_template, request
from PIL import Image, ImageOps 
app = Flask(__name__)



#function to get primary color
def primary_color(file_path):
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



@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        img = request.files["raw_image"]      #getting file from the form
        color_list = primary_color(img.stream) #The file is not sent wholely over the internet, it is sent in chunks of data, and we read these chunks using this stream property.
        return render_template("base.html", color_list=color_list)
    return render_template("base.html") # If the method is not POST, then simply render the frontend, if the method is POST, we pass our image file to a function that evaluates it. 

if __name__ == "__main__":
    app.run(debug = True)
