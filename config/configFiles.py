
from dataclasses import dataclass
import os 



@dataclass(frozen=True)
class ConfigFiles: 
    @property
    def PORT(self):
        return int(os.getenv("PORT"))

    @property
    def USER(self):
        return os.getenv("USER")

    @property
    def PASSWORD(self):
        return os.getenv("PASSWORD")

    @property
    def HOST(self):
        return os.getenv("HOST")

    @property
    def NAME(self):
        return os.getenv("DB")

    @property
    def DATABASE_URI(self):
        return f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


