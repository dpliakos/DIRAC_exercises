"""The script  for the Task5."""

from Book import Book, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USER = "root"
PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "13306"
DATABASE = "DIRAC"

engine = None
session = None


def getEngine():
    """Connect to the mysql server."""
    global engine
    if (engine is None):
        conn = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD,
                                                              MYSQL_HOST,
                                                              MYSQL_PORT,
                                                              DATABASE)
        engine = create_engine(conn, echo=True)

    return engine


def initialize():
    """Create the required tables."""
    engine = getEngine()

    global session
    if (session is None):
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)


if __name__ == "__main__":
    initialize()
    transaction = session()

    book_1 = Book(title="My super book")
    book_2 = Book(title="Old book")

    transaction.add(book_1)
    transaction.add(book_2)
    transaction.commit()

    book_3 = Book(title="Python cook book")
    transaction.add(book_3)
    transaction.rollback()

    # current_book = transaction.query(Book).get(1)
    # print (current_book.title)

    books_to_delete = transaction.query(Book).filter_by(title='Old book').all()

    for book in books_to_delete:
        transaction.delete(book)

    transaction.commit()
    transaction.close()
