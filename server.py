from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from back.lib.funcs import get_disease_names_by_text, get_doctors_by_disease, get_treatments_by_disease

app = FastAPI()


@app.get("/api/diseases")
def api_endpoint_diseases(text: str = Query(...), max_diseases: int = Query(3), max_doctors: int = Query(2), max_treatments: int = Query(2)):
    result = {
        "result": [
            {
                'disease': str(d),
                'doctors': get_doctors_by_disease(d, max_doctors),
                'treatments': get_treatments_by_disease(d, max_treatments)
            }
            for d in get_disease_names_by_text(text, max_len=max_diseases)
        ]
    }
    print("Result:", result)
    return result


@app.get("/")
def root():
    return RedirectResponse("/index.html")


app.mount("/", StaticFiles(directory="front"))
