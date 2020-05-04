from fastapi import FastAPI, Query
from ..lib.funcs import get_disease_names
app = FastAPI()


@app.get("/diseases")
def root(text: str = Query(...), max_len: int = Query(5)):
    return {"diseases": get_disease_names(text, max_len=max_len)}