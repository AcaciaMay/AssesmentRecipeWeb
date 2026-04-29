from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    category = request.args.get("category", "")
    
    
    categories = query_db("SELECT DISTINCT Category FROM Recipes WHERE Category IS NOT NULL")

    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if category:
        sql = base_select + " WHERE Category = ?"
        recipes = query_db(sql, (category,))
    else:
        recipes = query_db(base_select)


    return render_template(
        "home.html", 
        recipes=recipes, 
        categories=categories, 
        selected_category=category
    )

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database='database.db')
        db.row_factory = sqlite3.Row  
    return db

@app.route("/category/<category>")
def filter_by_category(category):
    recipes_data = query_db("SELECT * FROM Recipes WHERE Category = ?", (category,))
    return render_template("filtered_recipes.html", Recipes=recipes_data, selected_category=category)

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


if __name__ == "__main__":
    app.run(debug=True)
