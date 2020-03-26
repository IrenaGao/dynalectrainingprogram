from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def test_route():
    user_details = {'name': 'John', 'email': 'john@doe.com'}

    return render_template('test.html', user_details=user_details)

if __name__ == "__main__":
    app.run(debug=True)