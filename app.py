from flask import Flask, render_template, request
from urllib.parse import unquote
import requests  # Import the requests library
# Create the flask app
app = Flask(__name__)

# Replace with your Spoonacular API key
API_KEY = '5a71526ebfd84a61be153295388b0055'  # Better to use environment variables for this

# Define the route for the "Home" button
@app.route('/home', methods=['GET'])
def home():
    # Render the main page with empty recipe list and search query
    return render_template('index.html', recipes=[], search_query='')

# Define the main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If a form is submitted
        query = request.form.get('search_query', '')
        if not query:
            # If the query is empty, return an empty recipe list
            return render_template('index.html', recipes=[], search_query=query)
        # Perform a search for recipes with the given query
        recipes = search_recipes(query)
        # Render the main page with the search results and the search query
        return render_template('index.html', recipes=recipes, search_query=query)

    # If it's a GET request or no form submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    # Perform a search for recipes with the decoded search query
    recipes = search_recipes(decoded_search_query)
    # Render the main page
    return render_template('index.html', recipes=recipes, search_query=decoded_search_query)

# Function to search for recipes based on the provided query
def search_recipes(query):
    if not query:
        return []  # Return early if the query is empty

    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    # Send a GET request to the Spoonacular API with the query parameters
    response = requests.get(url, params=params)  # Use requests.get
    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])  # Use .get to avoid KeyError
    return []

# Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    search_query = request.args.get('search_query', '')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    response = requests.get(url, params=params)  # Use requests.get
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')