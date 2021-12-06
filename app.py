from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/home/<name>')
def name(name):
    return render_template('home.html', name=name)

@app.route('/post/<int:post_id>')
def post(post_id):
    return 'Post ID is %s' % post_id

@app.route('/')
def index():
    return 'Method used: %s' % request.method

if __name__ == '__main__':
    app.run(debug=True)