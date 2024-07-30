from flask import Flask, render_template, request

app = Flask(__name__)



#function to get primary color
def primary_color(raw_image):
    pass





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
