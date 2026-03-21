from sqlalchemy.orm import Session

from database.session import get_db, engine

def test_get_db_returns_session():
    gen = get_db()
    db = next(gen)
    
    # NOTE: SQLAlchemy uses 'lazy connection handling', test works because
    # the connection does not get initialized UNTIL we call actions on the database, i.e.:
    # execute()
    # commit()
    # query()
    # connection()

    assert isinstance(db, Session)

    # cleanup
    try:
        next(gen)
    except StopIteration:
        pass

def test_session_is_bound_to_engine():
    gen = get_db()
    db = next(gen)

    assert db.bind == engine

    try:
        next(gen)
    except StopIteration:
        pass

# TODO: Write test to check if database connection closed.