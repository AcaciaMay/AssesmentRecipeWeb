from flask import Flask, g, render_template
import sqlite3

app = Flask(__name__)

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

@app.route("/recipes")
def list_recipes():
    recipes = query_db("SELECT * FROM Recipes")
    return render_template("recipes.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True, port=4000, host="0.0.0.0")
