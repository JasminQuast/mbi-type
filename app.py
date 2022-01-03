from flask import Flask, request, render_template, url_for
#import twitter_userTweets
#import numpy
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=["POST"])
def form():
    twittname = request.form.get("twittname")
    #twitt_type = twitter_userTweets.pred_class

    return render_template('form.html', twittname=twittname
                           #,twitt_type=''.format(twitt_type)
                                                  )

@app.route('/types')
def types():
    return render_template('types.html')


if __name__ == '__main__':
    app.run(debug=True)