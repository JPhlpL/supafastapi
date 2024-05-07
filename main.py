from fastapi import FastAPI
from decouple import config

url = config("SUPERBASE_URL")
apikey = config("SUPERBASE_APIKEY")

app = FastAPI()

@app.get("/")
def test():
    return {"msg": "Hello World"}

