import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



os.environ['DATABASE_URL'] = "postgres://wolhkxmhprxbtl:e512c06b0a9bc06a8d642b1bcb8d549357b0d808cbf5335f76188671b0671c06@ec2-34-239-241-25.compute-1.amazonaws.com:5432/d8f5k154eujsth"
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books ( isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added Book with isbn: {isbn} Title: {title}  author: {author}, {year}.")
    db.commit()

if __name__ == "__main__":
    main()
