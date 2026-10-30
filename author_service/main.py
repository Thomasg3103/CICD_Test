from fastapi import FastAPI, HTTPException

app = FastAPI()

AUTHORS = {
    "frank-herbert": {"name": "Frank Herbert", "country": "USA", "born": 1920},
    "ursula-le-guin": {"name": "Ursula Le Guin", "country": "USA", "born": 1929},
}


@app.get("/authors/{slug}")
def get_author(slug: str):
    author = AUTHORS.get(slug)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author