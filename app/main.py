from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

BASE_URL = "https://dummyjson.com"


@app.get("/")
def root():
    return {"message": "Mocking and Fixture's testing endpoints"}


@app.get("/recipes")
def list_recipes(limit: int = 25):
    response = requests.get(f"{BASE_URL}/recipes")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error in external API")
    recipes = response.json()
    return recipes[:limit]


@app.get("/recipes/{recipe_id}")
def search_recipe(recipe_id: int):
    response = requests.get(f"{BASE_URL}/recipes/{recipe_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error in external API")
    return response.json()


@app.post("/recipes")
def create_recipe(recipe: dict):
    response = requests.post(f"{BASE_URL}/recipes/add", json=recipe)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to create recipe"
        )
    return response.json()
