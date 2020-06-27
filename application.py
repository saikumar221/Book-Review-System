import os
import requests

from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from markupsafe import escape


app = Flask(__name__)


# Check for environment variable

os.environ['DATABASE_URL'] = "postgres://wolhkxmhprxbtl:e512c06b0a9bc06a8d642b1bcb8d549357b0d808cbf5335f76188671b0671c06@ec2-34-239-241-25.compute-1.amazonaws.com:5432/d8f5k154eujsth"
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#API request from Goodreads

@app.route('/lg1')
def lg1():
    return render_template("login1.html")
@app.route('/')
def index():
    if 'username' in session:
        books = db.execute("SELECT * FROM books LIMIT 50")
        return render_template("index.html", name=session['username'],books = books)
    return redirect(url_for('login'))

@app.route("/books", methods=['POST'])
def books():
    query = request.form['query']
    query = '%' +query +"%"
    select = request.form['select']
    if select == "year":
        books = db.execute("SELECT * FROM books WHERE year =:query",{"query": int(request.form['query'])})
    elif select == "isbn":
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :query",{"query": query})
    elif select == "author":
        books = db.execute("SELECT * FROM books WHERE author LIKE :query",{"query": query})
    elif select == "title":
        books = db.execute("SELECT * FROM books WHERE title LIKE :query",{"query": query})
    return render_template("index.html", name=session['username'],books = books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        newuser = request.form['username']
        password = request.form['password']
        if not db.execute("SELECT * FROM users WHERE username = :username", {"username": newuser}).rowcount == 0:
            return render_template("error.html", message="User name already exists")
        db.execute("INSERT INTO users (username, password) VALUES (:name, :pass)",
            {"name": newuser, "pass": password})
        db.commit()
        return redirect(url_for('login'))
    elif 'username' in session :
        return render_template("register.html",message="Currenty logges in as "+session['username'])
    return render_template("register.html",message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        newuser = request.form['username']
        password = request.form['password']
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": newuser}).rowcount == 0:
            return render_template("error.html", message="User doesnot exists,please register")
        if not password == (db.execute("SELECT * from users WHERE username = :username",{"username": newuser}).fetchone()).password:
            return render_template("error.html", message="Wrong password!")
        session['username'] = newuser
        return redirect(url_for('index'))
    elif 'username' in session :
        return redirect(url_for('index'))
    return render_template("login.html",message="")

@app.route('/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route("/books/<string:isbn>")
def book(isbn):
    """Lists details about a single Book."""
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :id", {"id": isbn}).fetchone()
    comments = db.execute("SELECT * FROM comments WHERE isbn = :id", {"id": isbn})
    name = str(session['username'])
    if book is None:
        return render_template("error.html", message="No such flight.")
    if not db.execute("SELECT * FROM comments WHERE username = :username and isbn= :isbn", {"username": name,"isbn":isbn}).rowcount == 0:
        return render_template("book.html", book=book,comments=comments,disable="disabled")
    return render_template("book.html", book=book,comments=comments,disable="")

@app.route("/post/<string:isbn>", methods=['POST'])
def post(isbn):
    name = str(session['username'])
    isbn = isbn
    comment = request.form['comment']
    db.execute("INSERT INTO comments (isbn,username,comment)VALUES (:isbn, :name,:comment)",{"isbn":isbn, "name":name, "comment":comment})
    db.commit()
    return redirect(url_for('book', isbn=isbn,disble=""))

@app.route("/profile/<string:name>",methods=['POST'])
def profile(name):
    comments = db.execute("SELECT * FROM comments WHERE username = :name", {"name": name})
    return render_template("profile.html", name=name, comments=comments)


if __name__ == "__main__":
    app.run()