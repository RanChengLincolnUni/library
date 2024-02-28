from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from datetime import datetime
import db_connector

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/listbooks")
def listbooks():
    connection = db_connector.connection()
    if not connection:
        return 'Fail to connect database', 500

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books;")
        bookList = cursor.fetchall()
        return render_template("booklist.html", booklist=bookList)


@app.route("/loanbook")
def loanbook():
    todaydate = datetime.now().date()
    connection = db_connector.connection()
    if not connection:
        return 'Fail to connect database', 500

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM borrowers;")
        borrowerList = cursor.fetchall()
        sql = """
            SELECT * FROM bookcopies
            inner join books on books.bookid = bookcopies.bookid
            WHERE bookcopyid not in (SELECT bookcopyid from loans where returned <> 1 or returned is NULL);
        """
        cursor.execute(sql)
        bookList = cursor.fetchall()

    return render_template(
        "addloan.html",
        loandate=todaydate,
        borrowers=borrowerList,
        books=bookList,
    )


@app.route("/loan/add", methods=["POST"])
def addloan():
    borrowerid = request.form.get('borrower')
    bookid = request.form.get('book')
    loandate = request.form.get('loandate')

    connection = db_connector.connection()
    if not connection:
        return 'Fail to connect database', 500

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",
            (
                borrowerid,
                bookid,
                str(loandate),
            ),
        )

    return redirect("/currentloans")


@app.route("/listborrowers")
def listborrowers():
    connection = db_connector.connection()
    if not connection:
        return 'Fail to connect database', 500

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM borrowers;")
        borrowerList = cursor.fetchall()

    return render_template("borrowerlist.html", borrowerlist=borrowerList)


@app.route("/currentloans")
def currentloans():
    connection = db_connector.connection()
    if not connection:
        return 'Fail to connect database', 500

    with connection.cursor() as cursor:
        sql = """ 
            select br.borrowerid, br.firstname, br.familyname,  
                    l.borrowerid, l.bookcopyid, l.loandate, l.returned, b.bookid, b.booktitle, b.author, 
                    b.category, b.yearofpublication, bc.format 
            from books b
                    inner join bookcopies bc on b.bookid = bc.bookid
                        inner join loans l on bc.bookcopyid = l.bookcopyid
                            inner join borrowers br on l.borrowerid = br.borrowerid
            order by br.familyname, br.firstname, l.loandate;
        """
        cursor.execute(sql)
        loanList = cursor.fetchall()

    return render_template("currentloans.html", loanlist=loanList)
