from typing import Any

from pydantic import BaseSettings, SecretStr, RedisDsn


class Settings(BaseSettings):
    bot_token: SecretStr
    admins: list[int]
    use_redis: bool

    redis_dsn: RedisDsn

    db_dialect: str
    db_user: str
    pg_password: SecretStr
    db_pass: SecretStr
    db_host: str
    db_name: str
    db_echo: bool

    min_amount: int
    default_amount: int
    max_amount: int
    amount_step: int
    currency: str

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "admins":
                return [int(x) for x in raw_val.split(',')]
            if field_name in ("form_countries", "form_currencies"):
                return [x for x in raw_val.split(',')]
            if field_name in ("fuel_types", "buyer_types",
                              "age_range_private", "age_range_entity",
                              "units_of_power", "freight_types"):
                return {pair.split(":")[0]: pair.split(":")[1] for pair in raw_val.split(",")}
            return cls.json_loads(raw_val)

        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
