from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from back.lib.funcs import get_disease_names_by_text, get_doctors_by_disease, get_treatments_by_disease

app = FastAPI()


@app.get("/api/diseases")
def root(text: str = Query(...), max_diseases: int = Query(3), max_doctors: int = Query(2), max_treatments: int = Query(2)):
    return {
        "result": [
            {
                'disease': d,
                'doctors': get_doctors_by_disease(d, max_doctors),
                'treatments': get_treatments_by_disease(d, max_treatments)
            }
            for d in get_disease_names_by_text(text, max_len=max_diseases)
        ]
    }

app.mount("/", StaticFiles(directory="front"))
