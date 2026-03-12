from sqlalchemy.orm import Session

from app.database2.schema import Users

class UserService:
    def __init__(self, session: Session):
        self._db = session

    def get_users(self) -> list | None:
        return self._db.query(Users.user_id, Users.email).distinct().all()
    
    def get_user(self, id) -> dict | None:
        return self._db.query(Users).filter(Users.user_id == id).first()
    
    def post_user(self, data) -> dict | None:
        try:
            user = Users(**data)
            user.is_active = True
            self._db.add(user)
            self._db.commit()
            return user
        except Exception:
            return None