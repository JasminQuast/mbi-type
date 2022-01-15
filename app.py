from flask import Flask, request, render_template
import twitter_getUser
import twitter_userTweets

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/types')
def types():
    return render_template('types.html')


@app.route('/form', methods=["POST"])
def form():
    twittname = request.form.get("twittname")
    error_found = twitter_getUser.error_check()
    if error_found:
        error_reason = twitter_getUser.error_reason()
        return render_template('form.html', error_found=error_found, error_reason=error_reason)
    else:
        real_name = twitter_getUser.real_name()
        prediction = twitter_userTweets.current_posts()
        create_year = twitter_userTweets.start_time()
        past_prediction = twitter_userTweets.past_posts()
        pred_not_possible = ""
        if past_prediction == "":
            pred_not_possible = "Sorry, an available prediction is not possible."
        description = twitter_userTweets.description(prediction)
        past_description = twitter_userTweets.description(past_prediction)

        return render_template('form.html', error_found=error_found, twittname=twittname, prediction=prediction,
                               real_name=real_name, past_prediction=past_prediction, create_year=create_year,
                               description=description, past_description=past_description,
                               pred_not_possible=pred_not_possible)


if __name__ == '__main__':
    app.run(debug=False)
