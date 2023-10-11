from fastapi import FastAPI
from use_model_PD_segmented import run_query

# Fix for some old sqlite version
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

tags_metadata = [
    {
        "name": "Asistent",
        "description": "Asistentu postaviš vprašanje v polju **query**. Ostala polja so za napredno uporabo.",
    }
]


app = FastAPI(
    title="PPDFT Asistent",
    description="**Asistent za pomoč pri izobraževanju PPDFT 😜**",
    version="0.1",
    openapi_tags=tags_metadata
)


DEFAULT_QUERY = "Pozdravljen! Predstavi se kot asistent za pomoč pri izobraževanje pranja denarja (PPDFT)"

@app.get("/", tags=["Asistent"])
async def vprasaj_asistenta(query = "", model = "gpt-3.5-turbo", temperature = 0, k = 1):

    if query is None or query == "":
        query = DEFAULT_QUERY

    (response, sources) = run_query(query, temperature, int(k), model)

    return {"response": response, "sources": sources}