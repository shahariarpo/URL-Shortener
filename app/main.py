from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from app import crud
from app.database import init_db, get_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="URL Shortener", lifespan= lifespan)
app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": "Invalid Request body"})

@app.get("/")
def root():
    return{"status": "ok"}


@app.get("/{code}")
def redirect(code: str, conn = Depends(get_db)):
    row = crud.get_by_code(conn, code)
    if row is None:
        raise HTTPException(status_code=404, detail="Short Url not found")
    crud.increment_access(conn, code)
    return RedirectResponse(url=row["url"])