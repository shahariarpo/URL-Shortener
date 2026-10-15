from fastapi import APIRouter, Depends, HTTPException, Response

from app import crud
from app.database import get_db
from app.utils import is_valid_url
from app.schema import UrlBody

router = APIRouter()

def get_row_or_404(conn, code: str):
    row = crud.get_by_code(conn, code)
    if row is None:
        raise HTTPException(status_code=404, detail="Short URL Not Found")
    return row

@router.post("/shorten", status_code=201)
def create_short_url(body: UrlBody, conn = Depends(get_db)):
    if not is_valid_url(body.url):
        raise HTTPException(status_code=400, detail="Invalid Url")
    row = crud.create_url(conn, body.url)
    return crud.row_to_dict(row)

@router.get("/shorten/{code}")
def get_short_url(code: str, conn = Depends(get_db)):
    row = get_row_or_404(conn, code)
    crud.increment_access(conn, code)
    return crud.row_to_dict(row)

@router.put("/shorten/{code}")
def update_short_url( code: str, body: UrlBody, conn = Depends(get_db)):
    get_row_or_404(conn, code)
    if not is_valid_url(body.url):
        raise HTTPException(status_code=400, detail="Invalid Url")
    row = crud.update_url(conn, code, body.url)
    return crud.row_to_dict(row)

@router.delete("/shorten/{code}", status_code=204)
def delete_short_url(code: str, conn = Depends(get_db)):
    get_row_or_404(conn, code)
    crud.delete_url(conn, code)
    return Response(status_code=204)

@router.get("/shorten/{code}/stats")
def get_stats(code: str, conn = Depends(get_db)):
    row = get_row_or_404(conn, code)
    return crud.row_to_dict(row, include_stats=True)