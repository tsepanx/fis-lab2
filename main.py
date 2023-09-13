import time

import psycopg

from typing import Annotated, Sequence

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda: time.sleep(10))

templates = Jinja2Templates(directory="templates")

PG_DB = "lab2_table"
PG_USER = "postgres"
PG_HOST = "138.68.111.88"
PG_PASSWORD = "QAQjfPEpWumx2x%CVt@^cK4m&"


def psql_conn():
    conn = psycopg.connect(dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST)
    return conn


def db_get(conn: psycopg.connection, query, params: dict | Sequence | None) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


@app.get("/")
@limiter.limit("5/second")
async def root(request: Request):
    return "OK"


@app.get("/login", response_class=HTMLResponse)
async def login():
    return FileResponse("login.html")


@app.post("/login-form/")
async def login_form(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    conn = psql_conn()
    query = "SELECT * FROM db_user WHERE password = %s"

    results = db_get(conn, query, (password,))
    print(results)

    if len(results) == 1 and results[0][1] == username:
        return templates.TemplateResponse("profile.html", {"request": request, "username": username, "id": 3})
    else:
        return HTMLResponse("<h1>ERror!</h1>", status_code=404)


@app.get("/profile/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "id": id
        }
    )
