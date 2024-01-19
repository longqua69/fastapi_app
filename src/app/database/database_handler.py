from sqlalchemy.orm import Query, Session

from app.database.schemas import User

def get_user_by_username(username: str, db_session: Session) -> Query:
    return db_session.query(User.id).filter(User.username == username).first()

def populate_user_table():
    pass