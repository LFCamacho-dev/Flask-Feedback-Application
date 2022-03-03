from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_PASSWORD = os.environ.get("DB_PASSWORD")

# region ENV CONFIG
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@127.0.0.1:5432/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ""
# endregion

app.config['SECRET_KEY'] = "fasdkfjaldskfufjasliasdfasdfkjdh"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.create_all()


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@ app.route('/')
def index():
    print(os.environ.get('DB_PASSWORD'))
    return render_template('index.html')


@ app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)

        if customer == "" or dealer == "":
            return render_template('index.html', message='Please enter required fields.')

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')

        return render_template('index.html', message='You have already submitted feedback.')


if __name__ == "__main__":
    app.run()
