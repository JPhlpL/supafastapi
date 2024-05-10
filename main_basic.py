# main.py
from fastapi import FastAPI, status, HTTPException, Depends
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel
import random

# Initialize FastAPI app
app = FastAPI()

# Initialize Supabase client
supabase: Client = create_client(config("SUPERBASE_URL"), config("SUPERBASE_KEY"))

# Your existing code for Marvel data CRUD operations
@app.get("/marvel_data/")
def get_characters():
    marvel_rest = supabase.table("marvel_data").select("*").execute()
    return marvel_rest

@app.get("/marvel_data/{id}")
def get_character(id: int):
    marvel_rest = supabase.table("marvel_data").select("*").eq("id", id).execute()
    return marvel_rest

class MarvelSchema(BaseModel):
    name: str
    description: str
    location: str
    
@app.post("/marvel_data/", status_code=status.HTTP_201_CREATED)
def create_character(marvel: MarvelSchema):
    id = random.randint(0, 10000000)
    marvel = supabase.table("marvel_data").insert({
        "id": id,
        "name": marvel.name,
        "description": marvel.description,
        "location": marvel.location
    }).execute()
    return marvel

@app.delete("/marvel_data/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marvel(id: str):
    marvel = supabase.table("marvel_data").delete().eq("id", id).execute()
    return marvel

# create put function for update
@app.put("/marvel_data/", status_code=status.HTTP_202_ACCEPTED)
def update_character(id: str, marvel: MarvelSchema):
    marvel = supabase.table("marvel_data").update({
        "name": marvel.name,
        "description": marvel.description,
        "location": marvel.location
    }).eq("id", id).execute()
    return marvel

# Run the app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
