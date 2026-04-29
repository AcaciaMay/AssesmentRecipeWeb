from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

# --- DATABASE HELPERS ---

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database='database.db')
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
        # Splits "Breakfast, Dessert" into ["Breakfast", "Dessert"]
        parts = [p.strip() for p in row['Category'].split(',')]
        category_set.update(parts)
    return sorted(list(category_set))

# --- ROUTES ---

@app.route("/")
def home():
    category = request.args.get("category", "")
    
    # Get the cleaned, unique list for the sidebar/dropdown
    categories = get_unique_categories()

    # Base SQL logic
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if category:
        # Use LIKE to find the category even if it's in a list (e.g., "Breakfast, Dessert")
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
    # Get the cleaned list so the sidebar remains populated on this page too
    categories = get_unique_categories()
    
    # Filter recipes where the category string contains the selected word
    recipes_data = query_db("SELECT * FROM Recipes WHERE Category LIKE ?", (f"%{category}%",))
    
    return render_template(
        "filtered_recipes.html", 
        recipes=recipes_data, 
        categories=categories,
        selected_category=category
    )

if __name__ == "__main__":
    app.run(debug=True)



