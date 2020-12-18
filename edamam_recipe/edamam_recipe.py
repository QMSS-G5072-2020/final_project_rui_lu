import requests
import json
import os
import pandas as pd
import numpy as np
app_key = os.environ.get("PRIVATE_API_KEY")
app_id = os.environ.get("PRIVATE_API_ID")

def obtain_recipe(app_key, app_id, q, to = 10, ingr = 10):
    """
    Using this obtain_recipe function to collect data from EDAMAM API.
    EDAMAM API provides 1.7+million nutritionally analyzed recipes.
    Check the status of the request, and tell the user if there exists an error.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your ingredient or a recipe name
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe

    Returns
    -------
    A json format of data collected from API

    Examples
    --------
    >>> obtain_recipe(app_key, app_id, q = 'chicken', to = 10, ingr = 10)
    <json>
        It contains json format data, and the following is the first several rows of it.
    {'q': 'chicken',
     'from': 0,
     'to': 10,
     'more': True,
     'count': 54176,
     'hits': [{'recipe': {'uri': 'http://www.edamam.com/ontologies/edamam.owl#recipe_b79327d05b8e5b838ad6cfd9576b30b6',
     ...}
    """
    try:
        r = requests.get(f"https://api.edamam.com/search?app_key={app_key}&app_id={app_id}&q={q}&to={to}&ingr={ingr}")
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        raw_recipe = r.json()
        return raw_recipe


def find_recipe(app_key, app_id, q, to=10, ingr=10):
    """
    Using this find_recipe function to provide the user with the dishes that can be made with their ingredient.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your ingredient or a recipe name
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe

    Returns
    -------
    A dataframe that contains the recipe name, its image, and the website that presents its detailed information.

    Examples
    --------
    >>> find_recipe = find_recipe(app_key, app_id, q = 'chicken', to = 10, ingr = 10)
    >>> find_recipe.columns.values.tolist()
    ['Recipe Name', 'Image', 'Detailed Infomation']
    """
    raw_recipe = obtain_recipe(app_key, app_id, q, to, ingr)
    # get the whole desciption of the recipes
    hits = raw_recipe['hits']
    result = []
    for hit in hits:
        result.append(hit['recipe'])

    # get all the recipe name, their images and detailed information
    recipe_name = []
    recipe_image = []
    detail_info = []
    i = 0
    for i in range(0, len(result)):
        recipe_name.append(result[i]['label'])
        recipe_image.append(result[i]['image'])
        detail_info.append(result[i]['shareAs'])
        i = i + 1

    # turn the three lists into a dataframe with Recipe Name, Image, Detailed Information as columns
    pd.set_option('max_colwidth', 200)
    output_recipe = pd.DataFrame({'Recipe Name': recipe_name,
                                  'Image': recipe_image,
                                  'Detailed Infomation': detail_info})

    return output_recipe


def ingredient(app_key, app_id, q, to=10, ingr=10):
    """
    Using this ingredient function to provide the user with the ingredients they need to make a dish.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your ingredient or a recipe name
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe

    Returns
    -------
    A dataframe that contains the ingredients in text, their weights, and their images.

    Examples
    --------
    >>> ingredient = ingredient(app_key, app_id, q = 'chicken', to = 10, ingr = 10)
    >>> ingredient.columns.values.tolist()
    ['text', 'weight', 'image']
    """
    raw_recipe = obtain_recipe(app_key, app_id, q, to, ingr)
    # there may be several recipes for one recipe name, so we choose the first one here
    expected_ingredient = raw_recipe['hits'][0]['recipe']['ingredients']

    text = []
    weight = []
    image = []

    for ingredients in expected_ingredient:
        text.append(ingredients['text'])
        weight.append(ingredients['weight'])
        image.append(ingredients['image'])

    ingredients = pd.DataFrame({'text': text,
                                'weight': weight,
                                'image': image})
    return ingredients

def recipe_labels(app_key, app_id, q, to = 10, ingr = 10, diet_label = True, health_label = True, caution = True):
    """
    Using this recipe_labels function to provide the user with the label of recipe that they are interested in.
    The user can choose among the diet labe, the health label and the caution.
    If they don't want to a certain label, they can input False to that parameter.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your recipe name
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe
    diet_label: a boolean to indicate whether the user wants to know this lable.
    health_label: a boolean to indicate whether the user wants to know this lable.
    caution: a boolean to indicate whether the user wants to know this lable.

    Returns
    -------
    A list that contains the labels that the user want to know.

    Examples
    --------
    >>> recipe_labels(app_key, app_id, q = 'Chicken Vesuvio', to = 10, ingr = 10, diet_label = True, health_label = True, caution = True)
    ['Low-Carb', 'Peanut-Free', 'Tree-Nut-Free', 'Sulfites']
    >>> recipe_labels(app_key, app_id, q = 'Chicken Vesuvio', to = 10, ingr = 10, diet_label = False, health_label = True, caution = True)
    ['Peanut-Free', 'Tree-Nut-Free', 'Sulfites']
    """
    raw_recipe = obtain_recipe(app_key, app_id, q, to, ingr)
    # there may be several recipes for one recipe name, so we choose the first one here
    expected_recipe = raw_recipe['hits'][0]['recipe']
    labels = []
    if diet_label == True:
        diet_label = expected_recipe['dietLabels']
        for diet in diet_label:
            labels.append(diet)
    if health_label == True:
        health_label = expected_recipe['healthLabels']
        for health in health_label:
            labels.append(health)
    if caution == True:
        cautions = expected_recipe['cautions']
        for caution in cautions:
            labels.append(caution)
    return labels


def nutrient(app_key, app_id, q, to=10, ingr=10):
    """
    Using this nutrient function to provide the user with the detailed nutrients in the dish that they want to make.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input a recipe name
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe

    Returns
    -------
    A dataframe that contains the category of the nutrient, its label, quantity and unit.

    Examples
    --------
    >>> nutrient = nutrient(app_key, app_id, q = 'Chicken Vesuvio', to = 10, ingr = 10)
    >>> nutrient.columns.values.tolist()
    ['Category', 'Label', 'Quantity', 'Unit']
    """
    raw_recipe = obtain_recipe(app_key, app_id, q, to, ingr)
    # there may be several recipes for one recipe name, so we choose the first one here
    expected_nutrient = raw_recipe['hits'][0]['recipe']['totalNutrients']

    category = []
    for key in expected_nutrient.keys():
        category.append(key)
    helping = []
    for value in expected_nutrient.values():
        helping.append(value)

    label = []
    quantity = []
    unit = []
    for helps in helping:
        label.append(helps['label'])
        quantity.append(helps['quantity'])
        unit.append(helps['unit'])
    nutrient = pd.DataFrame({'Category': category,
                             'Label': label,
                             'Quantity': quantity,
                             'Unit': unit})
    return nutrient

def my_favourite(app_key, app_id, q, to = 10, ingr = 10, save = []):
    """
    Using this my_favourite function to help the user to memorize which dishes they are interested in.
    Next time, when the user has the same ingredient, they can find what they have interest in before.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your ingredient or a recipe name
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe
    save = a list to input the index of the recipe the user was interested in when they got use the find_recipe function

    Returns
    -------
    A list that contains the recipe name that the user has interest in.

    Examples
    --------
    >>> my_favourite(app_key, app_id, q = 'chicken', to = 10, ingr = 10, save = [2, 4])
    ['Chicken Feet Stock', 'Persian Chicken']
    """
    output_recipe = find_recipe(app_key, app_id, q, to, ingr)
    my_favourite = []
    for index in save:
        favourite_name = output_recipe.iloc[index, 0]
        my_favourite.append(favourite_name)
    return my_favourite


def recommend(app_key, app_id, q, height, weight, to=10, ingr=10):
    """"
    When user has a problem in deciding the recipe, this function recommends them according to user's height and weight.
    It uses BMI to measure whether a person is underweight, normal or overweight.
    For those who are underweight, this function will recommend the user with the dish with highest calories.
    For those who are normal, this function will recommend the user with the dish with median calories.
    For those who are overweight, this function will recommend the user with the dish with lowest calories.

    Parameters
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your ingredient or a recipe name
    height: a float to indicate the height of the user in meters
    weight: a float to indicate the weight of the user in kilograms
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe

    Returns
    -------
    A dataframe that contains the recommended recipe name and its detailed information

    Examples
    --------
    >>> recommend = recommend(app_key, app_id, q = 'chicken',to = 10, ingr = 10, height = 1.66, weight = 56)
    >>> recommend.columns.values.tolist()
    ['Recommend Recipe', 'Detailed Information']
    """
    raw_recipe = obtain_recipe(app_key, app_id, q, to, ingr)
    hits = raw_recipe['hits']
    result = []
    for hit in hits:
        result.append(hit['recipe'])

    # extract the calories of each dish
    calories = []
    for i in range(0, len(result)):
        calories.append(result[i]['calories'])

    # calculate the BMI to measure the whether a person is underweight, normal or overweight.
    BMI = weight / (height * height)
    if BMI < 18.5:  # recommend recipe with highest calories for those who are underweight
        index_cal = calories.index(max(calories))
    elif BMI > 24.5:  # recommend recipe with lowest calories for those who are overweight
        index_cal = calories.index(min(calories))
    elif (BMI >= 18.5 and BMI <= 24.5):  # recommend recipe with median calories for those who are normal
        # if the number of recipes is even number, delete the max calorie to get the median
        if len(calories) % 2 == 0:
            del calories[calories.index(max(calories))]
        index_cal = calories.index(np.median(calories))

    recipe_name = result[index_cal]['label']
    detailed_info = result[index_cal]['shareAs']
    recommend_recipe = pd.DataFrame({'Recommend Recipe': [recipe_name],
                                     'Detailed information': [detailed_info]})
    return recommend_recipe


def party(app_key, app_id, q, num_of_people, to=10, ingr=10):
    """
    When the user is going to hold a part, and need the recipe that can provide enough food for the guests.
    This function can recommend the recipes that satisfy this need
    
    Parameters 
    ----------
    app_key: a string to input your application key
    app_id: a string to input your application id
    q: a string to input your ingredient or a recipe name
    num_of_people: an integer to input the number of people that will come to the party
    to: an integer to input the last result index of the recipes (default to 10)
    ingr: an integer to input the maximum number of ingredients that you want in your recipe
    
    Returns
    -------
    Returns a dataframe that contains the recipe name and its website address with detail information
    
    Examples
    --------
    >>> party = party(app_key, app_id, q = 'chicken', num_of_people = 6, to = 10, ingr = 10)
    >>> party.columns.values.tolist()
    ['Party Recipe', 'Detailed information']
    """
    raw_recipe = obtain_recipe(app_key, app_id, q, to, ingr)
    hits = raw_recipe['hits']
    result = []
    for hit in hits:
        result.append(hit['recipe'])

    servings = []
    for i in range(0, len(result)):
        servings.append(result[i]['yield'])

    index_serving = [servings.index(serving) for serving in servings if serving >= num_of_people]

    recipe_name = []
    detailed_info = []

    for i in range(0, len(index_serving)):
        recipe_name.append(result[i]['label'])
        detailed_info.append(result[i]['shareAs'])

    party_recipe = pd.DataFrame({'Party Recipe': recipe_name,
                                 'Detailed information': detailed_info})
    return party_recipe
