from core.config import config

def test_config():
    assert config.app_name == "DIA: Data Ingest API"
    assert config.app_maintainer == "Toasted-ctrl"
    assert config.app_version == "0.1.2"
    
    assert config.db_database != ""
    assert config.db_password != ""
    assert config.db_username != ""
    assert config.db_hostname != ""
    assert config.db_port != ""

    assert config.db_connection != ""
    assert config.db_type != ""

    assert config.database_url != ""