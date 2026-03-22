from sqlalchemy.orm import Session

from database.schema import Ingest

class DataService:
    def __init__(self, session: Session):
        self._db = session

    def post_data(self, data: list) -> list[dict] | None:
        """
        Return list if successful, returns None if the operation failed."""

        try:
            self._db.add_all([Ingest(**entry) for entry in data])
            self._db.commit()
            return data
        except Exception:
            self._db.rollback() # Rolling back in case operation fails.
            return None

    def get_sources(self) -> list[tuple[str, str]] | None:
        return self._db.query(Ingest.base_url, Ingest.url_ext).distinct().all()