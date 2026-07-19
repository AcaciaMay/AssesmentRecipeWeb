from flask import Flask, g, render_template, request, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


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



@app.route("/")
def home():
    category = request.args.get("category", "")
    
    
    categories = get_unique_categories()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
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
        selected_category=category
        )

@app.route("/category/<category>")
def filter_by_category(category):
    categories = get_unique_categories()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        categories=categories,
        selected_category=category
)

def get_unique_common():
    """Fetches, splits, and deduplicates common ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Common FROM Pantry WHERE Common IS NOT NULL")
    common_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Common'].split(',')]
        common_set.update(parts)
    return sorted(list(common_set))


@app.route("/common")
def function1(common):
    common = request.args.get("common", "")
    
    
    common = get_unique_common()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if common:
        
        sql = base_select + " WHERE Common LIKE ?"
        pantry = query_db(sql, (f"%{common}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        common=common,
        selected_common=common)

@app.route("/common/<common>")
def filter_by_common(common):
    common_items = get_unique_common()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        common=common_items,
        selected_common=common
)

def get_unique_vegetables():
    """Fetches, splits, and deduplicates vegetable ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Vegetables FROM Pantry WHERE Vegetables IS NOT NULL")
    vegetables_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Vegetables'].split(',')]
        vegetables_set.update(parts)
    return sorted(list(vegetables_set))


@app.route("/vegetables")
def function2(vegetables):
    vegetables = request.args.get("vegetables", "")
    
    
    vegetables = get_unique_vegetables()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    # 3. Dynamic multi-select search construction
    query_params = []
    if selected_ingredients:
        # Construct multi-stage conditions like: WHERE Ingredients LIKE ? AND Ingredients LIKE ?
        conditions = []
        for item in selected_ingredients:
            conditions.append("Ingredients LIKE ?")
            query_params.append(f"%{item}%")
        
        final_sql = f"{base_sql} WHERE {' AND '.join(conditions)}"
        recipes = query_db(final_sql, tuple(query_params))
    else:
        # Default behavior matches original layout: load all entries when zero filters are chosen
        recipes = query_db(base_sql)

    return render_template(
        "home.html", 
        recipes=recipes,                          # Replaces 'pantry' references inside your list cards
        sidebar_items=sidebar_data,               # Contains all structural menu options
        selected_ingredients=selected_ingredients # Remembers checkboxes across page reloads
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    sql = """
        SELECT 
            ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum,
            Title,
            Creator,
            Image,
            Ingredients
        FROM Recipes
        WHERE LOWER(Title) LIKE ? OR LOWER(Creator) LIKE ?
        ORDER BY Title ASC;
    """
    like_query = f"%{query}%"
    results = query_db(sql, (like_query, like_query))
    return render_template("search_results.html", results=results, query=query)



@app.route("/recipes/<recipeid>")
def recipe_detail(recipeid):
    sql = """
        SELECT 
            Title,
            Creator,
            Image,
            Ingredients,
            Category,
            Website,
            RecipeLink
        FROM Recipes
        WHERE RecipesID = ?
    """
    recipe = query_db(sql, (recipeid,), one=True)
    if not recipe:
        abort(404)
    return render_template("recipes.html", recipe=recipe)





@app.route("/recipe/recipeid/<recipeid>")
def recipe_by_recipeid(recipeid):
    sql = """
        SELECT Title, Creator, Image, Ingredients, Category, Website, Recipelink
        FROM Recipes
        WHERE RecipeID = ?;
    """
    result = query_db(sql, [recipeid], one=True)
    if result is None:
        return "Recipe not found", 404
    return render_template("recipe.html", recipe=result)


if __name__ == "__main__":
    app.run(debug=True)



