from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=["POST"])
def form():
    name = request.form.get("twittname")
    return render_template('form.html', name=name)

@app.route('/types')
def types():
    return render_template('types.html')


if __name__ == '__main__':
    app.run(debug=True)