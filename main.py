from fastapi import FastAPI
from use_model_PD_segmented import run_query

app = FastAPI()

DEFAULT_QUERY = "Pozdravljen! Predstavi se kot asistent za pomoč pri izobraževanje pranja denarja (PPDFT)"

@app.get("/")
async def root(query = DEFAULT_QUERY, model = "gpt-3.5-turbo", temperature = 0, k = 1):

    (response, sources) = run_query(query, temperature, k, model)

    return {"response": response, "sources": sources}