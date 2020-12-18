from edamam_recipe import __version__
from edamam_recipe import edamam_recipe
import pandas as pd
import pytest
import os
app_key = os.environ.get("PRIVATE_API_KEY")
app_id = os.environ.get("PRIVATE_API_ID")

def test_version():
    assert __version__ == '0.1.0'

def test_find_recipe():
    find_recipe = edamam_recipe.find_recipe(app_key, app_id, q = 'chicken', to = 10, ingr = 10)
    assert find_recipe.columns.values.tolist() == ['Recipe Name', 'Image', 'Detailed Infomation']

def test_ingredient():
    ingredient = edamam_recipe.ingredient(app_key, app_id, q = 'chicken', to = 10, ingr = 10)
    assert ingredient.columns.values.tolist() == ['text', 'weight', 'image']

def test_recipe_labels():
    recipe_labels = edamam_recipe.recipe_labels(app_key, app_id, q = 'Chicken Vesuvio', to = 10, ingr = 10, diet_label = False, health_label = True, caution = True)
    assert recipe_labels == ['Peanut-Free', 'Tree-Nut-Free', 'Sulfites']

def test_nutrient():
    nutrient = edamam_recipe.nutrient(app_key, app_id, q = 'Chicken Vesuvio', to = 10, ingr = 10)
    assert nutrient.columns.values.tolist() == ['Category', 'Label', 'Quantity', 'Unit']

def test_my_favourite():
    my_favorite = edamam_recipe.my_favourite(app_key, app_id, q = 'chicken', to = 10, ingr = 10, save = [2, 4])
    assert my_favorite == ['Chicken Feet Stock', 'Persian Chicken']

def test_recommend():
    recommend = edamam_recipe.recommend(app_key, app_id, q = 'chicken', to = 10, ingr = 10, height = 1.66, weight = 56)
    assert recommend.columns.values.tolist() == ['Recommend Recipe', 'Detailed Information']

def test_party():
    party = edamam_recipe.party(app_key, app_id, q = 'chicken', to = 10, ingr = 10, num_of_people = 6)
    assert party.columns.values.tolist() == ['Party Recipe', 'Detailed information']
