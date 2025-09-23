from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables or a .env file.
    
    Attributes:
        SQL_SERVER_USER (str): Username to connect to the SQL Server database.
        SQL_SERVER_PASSWORD (str): Password for the SQL Server database user.
        SQL_SERVER_HOST (str): Hostname or IP of the SQL Server instance.
        SQL_SERVER_PORT (int): Port number of the SQL Server instance.
        SQL_SERVER_DB (str): Name of the database to connect to.
        SQL_SERVER_DRIVER (str): ODBC driver used for connecting to SQL Server.
        SECRET_KEY (str): Secret key used for JWT token encoding/decoding and other security-related operations.
        ALGORITHM (str): Algorithm used for JWT token encoding/decoding.
    """

    SQL_SERVER_USER: str
    SQL_SERVER_PASSWORD: str
    SQL_SERVER_HOST: str
    SQL_SERVER_PORT: int
    SQL_SERVER_DB: str
    SQL_SERVER_DRIVER: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        """
        Configuration for Pydantic Settings.
        
        Attributes:
            env_file (str): Name of the file from which to load environment variables.
        """
        env_file = ".env"


# Create a singleton instance of Settings to be used throughout the app
settings = Settings()