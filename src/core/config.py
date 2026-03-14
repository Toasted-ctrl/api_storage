from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    app_name: str = "DIA: Data Ingest API"
    app_maintainer: str = "Toasted-ctrl"
    app_version: str = "0.1.1"

    # NOTE: These will autopopulate as the BaseSettings class imports matching load_dotenv() values automatically.
    db_hostname: str = ""
    db_password: str = ""
    db_username: str = ""
    db_type: str = ""
    db_connection: str = ""
    db_port: str = ""
    db_database: str = ""

    @property
    def database_url(self):
        return f"{self.db_type}+{self.db_connection}://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"

config = Config()