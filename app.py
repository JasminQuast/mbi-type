from flask import Flask, request, render_template, url_for, jsonify
#import twitter_userTweets
#import numpy as np #2.
#import pickle #2.

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb')) #2.

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=["POST"])
def form():
    twittname = request.form.get("twittname")
    #twitt_type = twitter_userTweets.pred_class
    return render_template('form.html', twittname=twittname
                           #,twitt_type=''.format(twitt_type)
                           #, twitt_type=twitt_type
                                                  )
    # Get the data from the POST request. #2.:
    #data = request.get_json(force=True)
    # Make prediction using model loaded from disk as per the data.
    #prediction = model.predict([[np.array(twittname)]])
    # Take the first value of prediction
    #output = prediction[0]
    #return jsonify(output)

@app.route('/types')
def types():
    return render_template('types.html')


if __name__ == '__main__':
    app.run(debug=True)