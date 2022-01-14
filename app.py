from flask import Flask, request, render_template
import twitter_getUser
import twitter_userTweets

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/form', methods=["POST"])
def form():
    twittname = request.form.get("twittname")
    error_found = twitter_getUser.errorCheck()
    if error_found:
        error_reason = twitter_getUser.error_reason()
        return render_template('form.html', error_found=error_found, error_reason=error_reason)
    else:
        prediction = twitter_userTweets.pred()
        past_prediction = twitter_userTweets.past_ped()
        real_name = twitter_getUser.realName()
        create_year = twitter_userTweets.start_time()
        return render_template('form.html', error_found=error_found, twittname=twittname, prediction=prediction,
                               real_name=real_name, past_prediction=past_prediction, create_year=create_year)


@app.route('/types')
def types():
    return render_template('types.html')


if __name__ == '__main__':
    app.run(debug=False)
