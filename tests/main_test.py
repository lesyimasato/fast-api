import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_recipe_data():
    return [
        {
            "id": 1,
            "name": "Mocked Greek Salad",
            "ingredients": ["Tomatoes", "Cucumber", "Onion", "Feta Cheese", "Olives"],
            "instructions": [
                "Chop the vegetables.",
                "Mix together in a bowl.",
                "Add feta and olives before serving.",
            ],
            "prepTimeMinutes": 15,
            "cookTimeMinutes": 0,
            "servings": 2,
            "difficulty": "Easy",
            "cuisine": "Greek",
            "caloriesPerServing": 200,
            "tags": ["Salad", "Healthy", "Vegetarian"],
            "image": "https://cdn.dummyjson.com/recipe-images/1.webp",
        },
        {
            "id": 2,
            "name": "Mocked Spaghetti Bolognese",
            "ingredients": [
                "Spaghetti",
                "Ground beef",
                "Tomato sauce",
                "Onion",
                "Garlic",
            ],
            "instructions": [
                "Cook spaghetti according to package instructions.",
                "Brown the beef with onion and garlic.",
                "Add tomato sauce and simmer.",
                "Serve sauce over spaghetti.",
            ],
            "prepTimeMinutes": 10,
            "cookTimeMinutes": 30,
            "servings": 4,
            "difficulty": "Medium",
            "cuisine": "Italian",
            "caloriesPerServing": 550,
            "tags": ["Pasta", "Main Course"],
            "image": "https://cdn.dummyjson.com/recipe-images/2.webp",
        },
    ]


@pytest.fixture
def mock_individual_recipe():
    return {
        "id": 1,
        "name": "Mocked Greek Salad",
        "ingredients": ["Tomatoes", "Cucumber", "Onion", "Feta Cheese", "Olives"],
        "instructions": [
            "Chop the vegetables.",
            "Mix together in a bowl.",
            "Add feta and olives before serving.",
        ],
        "prepTimeMinutes": 15,
        "cookTimeMinutes": 0,
        "servings": 2,
        "difficulty": "Easy",
        "cuisine": "Greek",
        "caloriesPerServing": 200,
        "tags": ["Salad", "Healthy", "Vegetarian"],
        "image": "https://cdn.dummyjson.com/recipe-images/1.webp",
        "userId": 1,
    }


@pytest.fixture
def mock_success_requests(mocker):
    def _mock(data, status_code=200):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = data
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock


@pytest.fixture
def mock_success_post_requests(mocker):
    def _mock(data, status_code=200):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = data
        mocker.patch("requests.post", return_value=mock_response)
        return mock_response

    return _mock


@pytest.fixture
def mock_error_requests(mocker):
    def _mock(status_code=500):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock


# test using fixtures with mocking
def test_get_all_recipes_success(client, mock_recipe_data, mock_success_requests):
    mock_success_requests(mock_recipe_data)

    response = client.get("/recipes?limit=2")

    assert response.status_code == 200
    assert response.json() == mock_recipe_data


def test_get_recipe_by_id(client, mock_individual_recipe, mock_success_requests):
    mock_success_requests(mock_individual_recipe)

    response = client.get("/recipes/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Mocked Greek Salad"


def test_post_recipe_success(client, mock_success_post_requests):
    new_recipe = {
        "name": "Mocked Soup",
        "ingredients": ["Water"],
        "instructions": "Boil",
    }
    mock_success_post_requests({"id": 10, "name": "Mocked Soup"})

    response = client.post("/recipes", json=new_recipe)

    assert response.status_code == 200
    assert response.json()["name"] == "Mocked Soup"


def test_get_recipes_error(client, mock_error_requests):
    mock_error_requests(status_code=500)

    response = client.get("/recipes")

    assert response.status_code == 500
    assert "erro" in response.json()["detail"].lower()


def test_get_recipe_not_found(client, mock_error_requests):
    mock_error_requests(status_code=404)

    response = client.get("/recipes/999")

    assert response.status_code == 404
    assert "recipe not found" in response.json()["detail"].lower()
