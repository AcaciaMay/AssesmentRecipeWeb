from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)



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
        
        parts = [p.strip() for p in row['Category'].split(',')]
        category_set.update(parts)
    return sorted(list(category_set))


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
    
    recipes_data = query_db("SELECT * FROM Recipes WHERE Category LIKE ?", (f"%{category}%",))
    
    return render_template(
        "filtered_recipes.html", 
        recipes=recipes_data, 
        categories=categories,
        selected_category=category
    )

if __name__ == "__main__":
    app.run(debug=True)



