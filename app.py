from flask import Flask, request, render_template
import twitter_userTweets

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/form', methods=["POST"])
def form():
    twittname = request.form.get("twittname")
    prediction = twitter_userTweets.pred()

    return render_template('form.html', twittname=twittname, prediction=prediction)


@app.route('/types')
def types():
    return render_template('types.html')


if __name__ == '__main__':
    app.run(debug=False)
