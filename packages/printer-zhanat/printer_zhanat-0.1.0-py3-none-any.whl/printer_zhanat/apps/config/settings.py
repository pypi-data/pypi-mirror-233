from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VENDOR_ID: Any = 0x0dd4
    PRODUCT_ID: Any = 0x015d


settings = Settings()
