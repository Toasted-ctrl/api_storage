from sqlalchemy.orm import Session

from src.database.schema import Ingest

class DataService:
    def __init__(self, session: Session):
        self._db = session

    def post_data(self, data: list) -> list[dict] | None:
        """
        Return list if successful, returns None if the operation failed."""

        try:
            self._db.add_all([Ingest(**entry) for entry in data])
            self._db.commit()
            self._db.refresh()
            return data
        except Exception:
            return None

    def get_sources(self) -> dict | None:
        return self._db.query(Ingest.base_url, Ingest.url_ext).distinct().all()