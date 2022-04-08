import uvicorn
from fastapi import FastAPI
from dotenv import dotenv_values
from typing import Optional, Dict, Any

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

app = FastAPI()


@app.get("/test")
async def test() -> Dict[str, str]:
    return {"message": "test"}


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> Dict[str, Any]:
    """Multiplication de deux nombres entiers.

    Cette fonction ne sert pas à grand chose.

    Parameters
    ----------
    item_id : int
        Le premier nombre entier.
    nombre2 : int
        Le second nombre entier.

        Avec une description plus longue.
        Sur plusieurs lignes.

    Returns
    -------
    int
        Le produit des deux nombres.
    """
    return {"item_id": item_id, "q": q}


def start() -> None:
    print(config["MONNGO_VERSION"])
    """Launched with `poetry run start` at root level"""
    uvicorn.run("retails_analysis.dispatch:app", host="0.0.0.0", port=8000, reload=True)
