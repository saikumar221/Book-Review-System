Book Review System
https://booksreview-project1.herokuapp.com/
This is a website built using Flask Framework and PostgreSQL databse.
Users can register providing a username and password.
Users, once registered, Can log in to the website with their username and password.
Logged in users should be able to log out of the site.(as i used sessions for this)
Import.py file is used to upload the data from .csv file into the PostgreSQL database which is on Heroku.
Once a user has logged in, they should will be taken to a page where they can search for a book. Users can type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, website will display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name,  search page will find matches for those as well!
When users click on a book from the results of the search page, they will be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
On the book page, users can submit a (*in progress -review: consisting of a rating on a scale of 1 to 5*), as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
(*In progress Goodreads Review Data: On book page, display (if available) the average rating and number of ratings the work has received from Goodreads.
API Access: If users make a GET request to website’s /api/<isbn> route, where <isbn> is an ISBN number,website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.*)
