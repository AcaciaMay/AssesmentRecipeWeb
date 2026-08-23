from flask import Flask, g, render_template, request, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

@app.context_processor
def inject_dropdown_data():
    # This automatically makes 'dropdown_data' available to EVERY HTML template, including search_results.html
    return {
        "dropdown_data": {
            "common_ingredients": get_unique_common(),
            "vegetables": get_unique_vegetables(),
            "meats": get_unique_meats(),
            "dairy": get_unique_dairy(),
            "mushrooms": get_unique_mushrooms(),
            "herbs": get_unique_herbs(),
            "nuts_grains": get_unique_nuts_grains(), # Ensure key matches template exactly
            "miscellaneous": get_unique_miscellaneous()
        }
    }


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_unique_categories():
    """Fetches, splits, and deduplicates categories from the DB."""
    raw_data = query_db("SELECT DISTINCT Category FROM Recipes WHERE Category IS NOT NULL")
    category_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Category'].split(',')]
        category_set.update(parts)
    return sorted(list(category_set))


def get_unique_common():
    """Fetches, splits, and deduplicates common ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Common FROM Pantry WHERE Common IS NOT NULL")
    common_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Common'].split(',')]
        common_set.update(parts)
    return sorted(list(common_set))


def get_unique_vegetables():
    """Fetches, splits, and deduplicates vegetable ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Vegetables FROM Pantry WHERE Vegetables IS NOT NULL")
    vegetables_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Vegetables'].split(',')]
        vegetables_set.update(parts)
    return sorted(list(vegetables_set))



def get_unique_meats():
    """Fetches, splits, and deduplicates meat ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Meats FROM Pantry WHERE Meats IS NOT NULL")
    Meats_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Meats'].split(',')]
        Meats_set.update(parts)
    return sorted(list(Meats_set))



def get_unique_dairy():
    """Fetches, splits, and deduplicates dairy ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Dairy FROM Pantry WHERE Dairy IS NOT NULL")
    dairy_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Dairy'].split(',')]
        dairy_set.update(parts)
    return sorted(list(dairy_set))


def get_unique_baking():
    """Fetches, splits, and deduplicates baking ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Baking FROM Pantry WHERE Baking IS NOT NULL")
    baking_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Baking'].split(',')]
        baking_set.update(parts)
    return sorted(list(baking_set))



def get_unique_fruits():
    """Fetches, splits, and deduplicates fruit ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Fruits FROM Pantry WHERE Fruits IS NOT NULL")
    fruits_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Fruits'].split(',')]
        fruits_set.update(parts)
    return sorted(list(fruits_set))


def get_unique_mushrooms():
    """Fetches, splits, and deduplicates mushroom ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Mushrooms FROM Pantry WHERE Mushrooms IS NOT NULL")
    mushrooms_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Mushrooms'].split(',')]
        mushrooms_set.update(parts)
    return sorted(list(mushrooms_set))


def get_unique_herbs():
    """Fetches, splits, and deduplicates herb ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Herbs FROM Pantry WHERE Herbs IS NOT NULL")
    herbs_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Herbs'].split(',')]
        herbs_set.update(parts)
    return sorted(list(herbs_set))

def get_unique_nuts_grains():
    """Fetches, splits, and deduplicates nuts_grains safely from the DB."""
    # FIX: Wrapped in square brackets so SQLite allows the '&' symbol
    raw_data = query_db("SELECT DISTINCT [Nuts_Grains] FROM Pantry WHERE [Nuts_Grains] IS NOT NULL")
    nuts_grains_set = set()
    for row in raw_data:
        # FIX: Matches the exact column string wrapper key name
        parts = [p.strip() for p in row['Nuts_Grains'].split(',')]
        nuts_grains_set.update(parts)
    return sorted(list(nuts_grains_set))



def get_unique_miscellaneous():
    """Fetches, splits, and deduplicates miscellaneous ingredients safely from the DB."""
    raw_data = query_db("SELECT DISTINCT [Miscellaneous] FROM Pantry WHERE [Miscellaneous] IS NOT NULL")
    misc_set = set()
    for row in raw_data:
        parts = [p.strip() for p in row['Miscellaneous'].split(',')]
        misc_set.update(parts)
    return sorted(list(misc_set))



@app.route("/")
def home():
    category = request.args.get("category", "")
    categories = get_unique_categories()
    
    # Pre-populate all the multi-select lists for your dropdown menus
    dropdown_data = {
        "common_ingredients": get_unique_common(),
        "vegetables": get_unique_vegetables(),
        "meats": get_unique_meats(),
        "dairy": get_unique_dairy(),
        # New functions matching your database screenshot names:
        "mushrooms": get_unique_mushrooms(),
        "herbs": get_unique_herbs(),
        "nuts_grains": get_unique_nuts_grains(),
        "miscellaneous": get_unique_miscellaneous()
    }
    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, AllergyWarning, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, AllergyWarning, Website 
              FROM Recipes)
    """

    if category:
        sql = base_select + " WHERE Category LIKE ?"
        recipes = query_db(sql, (f"%{category}%",))
    else:
        recipes = query_db(base_select)

    return render_template(
        "home.html", 
        recipes=recipes, 
        categories=categories, 
        selected_category=category,
        dropdown_data=dropdown_data,
        selected_ingredients=[] # Emptied on normal home load
    )


@app.route("/filter")
def filter_recipes():
    selected_ingredients = request.args.getlist("ingredient")
    
    if selected_ingredients:
        match_score_clauses = " + ".join(["(CASE WHEN Ingredients LIKE ? THEN 1 ELSE 0 END)" for _ in selected_ingredients])
        where_clauses = " OR ".join(["Ingredients LIKE ?" for _ in selected_ingredients])
        
        sql = f"""
            SELECT RecipeID, Title, Creator, Image, Ingredients, Category, Website, AllergyWarning,
                   ({match_score_clauses}) AS MatchCount
            FROM (
                SELECT RecipeID, Title, Creator, Image, Ingredients, Category, AllergyWarning, Website 
                FROM Recipes
            )
            WHERE {where_clauses}
            ORDER BY MatchCount DESC, Title ASC
        """
        query_params = [f"%{item}%" for item in selected_ingredients] * 2
        recipes = query_db(sql, tuple(query_params))
    else:
        sql = """
            SELECT RecipeID, Title, Creator, Image, Ingredients, Category, Website, AllergyWarning
            FROM Recipes
            ORDER BY Title ASC
        """
        recipes = query_db(sql)

    return render_template(
        "home.html", 
        recipes=recipes, 
        categories=get_unique_categories(), 
        selected_category="",
        selected_ingredients=selected_ingredients
    )



@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()

    # FIXED: Cleaned up the CASE WHEN statement syntax
    sql = """
        SELECT 
            RecipeID,
            Title,
            Creator,
            Image,
            Ingredients
        FROM Recipes
        WHERE Title LIKE ? OR Ingredients LIKE ?
        ORDER BY 
            (CASE WHEN Title LIKE ? THEN 0 ELSE 1 END) ASC,
            Title ASC;
    """
    
    like_anywhere = f"%{query}%"
    like_start = f"{query}%" 
    results = query_db(sql, (like_anywhere, like_anywhere, like_start))
    
    # If no recipes match the search query, show your custom error page!
    if not results:
        return render_template("error.html", query=query), 404
    
    return render_template(
        "search_results.html", 
        recipes=results, 
        query=query, 
        categories=get_unique_categories(),
        selected_category=""
    )


@app.route("/recipes/<recipeid>")
def recipe_detail(recipeid):
    sql = """
        SELECT RecipeID, Title, Creator, Image, Ingredients, Category, Website, AllergyWarning, RecipeLink
        FROM Recipes
        WHERE RecipeID = ?
    """
    recipe = query_db(sql, (recipeid,), one=True)
    if not recipe:
        abort(404)
    return render_template("recipe.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True, port=4567, host="0.0.0.0")
