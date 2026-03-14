from sqlalchemy.orm import Session

from auth.generate_key import generate_keys
from database.schema import Users, ApiKeys

class UserService:
    def __init__(self, session: Session):
        self._db = session

    def get_users(self) -> list | None:
        return self._db.query(Users.user_id, Users.email).distinct().all()
    
    def _check_key_unique(self, key: str) -> bool:

        """
        Verifies whether the generated key already exists in the api_keys table. Will return True if the
        key is unique.
        """

        return (self._db.query(ApiKeys.hashed_api_key)
                .filter(ApiKeys.hashed_api_key == key)
                .scalar()) is None
    
    def _create_keys(self) -> tuple[str, str]:

        """
        Will create a set of keys and ensure the hashed version does not already exist in the database.
        """

        unhashed_key, hashed_key = generate_keys()
        if self._check_key_unique(key=hashed_key):
            return (unhashed_key, hashed_key)
        
        # NOTE: Recursive function, might cause the server to hang if we keep generating non-uniques.
        # TODO: Investigate a potential better solution.
        return self._create_keys()
    
    def get_user(self, id: int) -> dict | None:
        return self._db.query(Users).filter(Users.user_id == id).first()
    
    def post_user(self, data: dict) -> tuple[dict, str] | None:

        """
        Returns none if failed to post user, returns a tuple with:
        [0]: added user dict
        [1]: unhashed api key
        """

        try:
            unhashed_key, hashed_key = self._create_keys()
                
            user = Users(**data)
            user.is_active = True
            self._db.add(user)
            self._db.commit()

            keys = ApiKeys(hashed_api_key=hashed_key, user_id=user.user_id)
            self._db.add(keys)
            self._db.commit()

            return user, unhashed_key
        
        except Exception:
            return None