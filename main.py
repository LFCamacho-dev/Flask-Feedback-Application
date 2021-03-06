from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from send_mail import send_mail


load_dotenv()

app = Flask(__name__)

DB_PASSWORD = os.environ.get("DB_PASSWORD")

# region ENV CONFIG
ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@127.0.0.1:5432/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://smzjpppvfdecho:8d4f1604479e30ffa593ef09b65b1746373d2322eb07bececfcf65cd7178a669@ec2-3-225-79-57.compute-1.amazonaws.com:5432/d98q37bbd3dcer"
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

            send_mail(customer, dealer, rating, comments)

            return render_template('success.html')

        return render_template('index.html', message='You have already submitted feedback.')


if __name__ == "__main__":
    app.run()
