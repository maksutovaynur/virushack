from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from back.lib.funcs import get_disease_names_by_text, get_doctor_by_disease, get_treatments_by_disease

app = FastAPI()


@app.get("/api/diseases")
def root(text: str = Query(...), max_len: int = Query(5)):
    return {
        "result": [
            {
                'disease': d,
                'doctor': get_doctor_by_disease(disease_name=d),
                'treatments': get_treatments_by_disease(d)
            }
            for d in get_disease_names_by_text(text, max_len=max_len)
        ]
    }

app.mount("/", StaticFiles(directory="front"))
