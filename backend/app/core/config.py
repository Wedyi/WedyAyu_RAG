from pydantic import Secret
from pydantic_settings import SettingsConfigDict,BaseSettings
from typing import Optional
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")
    Database_URL: Optional[str] = None
    Secret_Key: Optional[str] = None
    API_KEY: Optional[str] = None
    base_url: Optional[str] = None

settings = Settings()



if __name__ == "__main__":
    print(settings.Database_URL)
    print(settings.Secret_Key)
    print(settings.API_KEY)
    print(settings.base_url)        