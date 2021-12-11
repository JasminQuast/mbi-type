from flask import Flask, request, render_template

app = Flask(__name__)

# def index():
#     name= "Jasmin"
#     return render_template("home.html", name=name)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/types')
def types():
    return render_template('types.html')


if __name__ == '__main__':
    app.run(debug=True)