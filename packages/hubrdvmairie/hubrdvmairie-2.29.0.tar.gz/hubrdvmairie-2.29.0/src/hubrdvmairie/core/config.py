import logging
import os
from functools import lru_cache
from typing import Set

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    debug: bool
    api_prefix: str = "/api"
    project_name: str = "HUB RDV"

    logging_level: int = 0
    loggers: Set[str] = {"uvicorn.asgi", "uvicorn.access"}

    editors_list = []
    meeting_point_list = []
    offline_meeting_point_list = []
    ws_use_rates = {}

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("debug")
    def set_name(cls, debug):
        return debug or False


@lru_cache()
def get_settings() -> Settings:
    debug = os.environ.get("ENVIRONMENT") not in ["dev", "preprod"]
    settings = Settings(debug=debug)
    settings.logging_level = logging.DEBUG if debug else logging.INFO
    return settings
