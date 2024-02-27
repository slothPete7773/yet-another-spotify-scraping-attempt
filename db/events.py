from fastapi import FastAPI


async def connect_to_db(app: FastAPI, setting: dict) -> None:
    pass


async def close_db_connection(app: FastAPI) -> None:
    pass
