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

    if vegetables:
        
        sql = base_select + " WHERE Vegetables LIKE ?"
        pantry = query_db(sql, (f"%{vegetables}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        vegetables=vegetables,
        selected_vegetables=vegetables)

@app.route("/vegetables/<vegetables>")
def filter_by_vegetables(vegetables):
    vegetables_items = get_unique_vegetables()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        vegetables=vegetables_items,
        selected_vegetables=vegetables
)



def get_unique_meat():
    """Fetches, splits, and deduplicates meat ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Meat FROM Pantry WHERE Meat IS NOT NULL")
    Meat_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Meat'].split(',')]
        Meat_set.update(parts)
    return sorted(list(Meat_set))


@app.route("/meat")
def function3(meat):
    meat = request.args.get("meat", "")
    
    
    meat = get_unique_meat()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if meat:
        
        sql = base_select + " WHERE Meat LIKE ?"
        pantry = query_db(sql, (f"%{meat}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        meat=meat,
        selected_meat=meat)

@app.route("/meat/<meat>")
def filter_by_meat(meat):
    meat_items = get_unique_meat()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        meat=meat_items,
        selected_meat=meat
)


def get_unique_dairy():
    """Fetches, splits, and deduplicates dairy ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Dairy FROM Pantry WHERE Dairy IS NOT NULL")
    dairy_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Dairy'].split(',')]
        dairy_set.update(parts)
    return sorted(list(dairy_set))


@app.route("/dairy")
def function4(dairy):
    dairy = request.args.get("dairy", "")
    
    
    dairy = get_unique_dairy()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if dairy:
        
        sql = base_select + " WHERE Dairy LIKE ?"
        pantry = query_db(sql, (f"%{dairy}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        dairy=dairy,
        selected_dairy=dairy)

@app.route("/dairy/<dairy>")
def filter_by_dairy(dairy):
    dairy_items = get_unique_dairy()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        dairy=dairy_items,
        selected_dairy=dairy
)


def get_unique_baking():
    """Fetches, splits, and deduplicates baking ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Baking FROM Pantry WHERE Baking IS NOT NULL")
    baking_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Baking'].split(',')]
        baking_set.update(parts)
    return sorted(list(baking_set))


@app.route("/baking")
def function5(baking):
    baking = request.args.get("baking", "")
    
    
    baking_items = get_unique_baking()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if baking:
        
        sql = base_select + " WHERE Baking LIKE ?"
        pantry = query_db(sql, (f"%{baking}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        baking=baking,
        selected_baking=baking)

@app.route("/baking/<baking>")
def filter_by_baking(baking):
    baking_items = get_unique_baking()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        baking=baking_items,
        selected_baking=baking
)


def get_unique_fruits():
    """Fetches, splits, and deduplicates fruit ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Fruits FROM Pantry WHERE Fruits IS NOT NULL")
    fruits_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Fruits'].split(',')]
        fruits_set.update(parts)
    return sorted(list(fruits_set))


@app.route("/fruits")
def function6(fruits):
    fruits = request.args.get("fruits", "")
    
    
    fruits = get_unique_fruits()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if fruits:
        
        sql = base_select + " WHERE Fruits LIKE ?"
        pantry = query_db(sql, (f"%{fruits}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        fruits=fruits,
        selected_fruits=fruits)

@app.route("/fruits/<fruits>")
def filter_by_fruits(fruits):
    fruits_items = get_unique_fruits()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        fruits=fruits_items,
        selected_fruits=fruits
)

def get_unique_mushrooms():
    """Fetches, splits, and deduplicates mushroom ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Mushrooms FROM Pantry WHERE Mushrooms IS NOT NULL")
    mushrooms_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Mushrooms'].split(',')]
        mushrooms_set.update(parts)
    return sorted(list(mushrooms_set))



@app.route("/mushrooms")
def function7(mushrooms):
    mushrooms = request.args.get("mushrooms", "")
    
    
    mushrooms = get_unique_mushrooms()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if mushrooms:
        sql = base_select + " WHERE Mushrooms LIKE ?"
        pantry = query_db(sql, (f"%{mushrooms}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        mushrooms=mushrooms,
        selected_mushrooms=mushrooms)

@app.route("/mushrooms/<mushrooms>")
def filter_by_mushrooms(mushrooms):
    mushrooms_items = get_unique_mushrooms()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        mushrooms=mushrooms_items,
        selected_mushrooms=mushrooms
)

def get_unique_herbs():
    """Fetches, splits, and deduplicates herb ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Herbs FROM Pantry WHERE Herbs IS NOT NULL")
    herbs_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Herbs'].split(',')]
        herbs_set.update(parts)
    return sorted(list(herbs_set))


@app.route("/herbs")
def function8(herbs):
    herbs = request.args.get("herbs", "")

    
    
    herbs = get_unique_herbs()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if herbs:
        
        sql = base_select + " WHERE Herbs LIKE ?"
        pantry = query_db(sql, (f"%{herbs}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        herbs=herbs,
        selected_herbs=herbs)

@app.route("/herbs/<herbs>")
def filter_by_herbs(herbs):
    herbs_items = get_unique_herbs()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        herbs=herbs_items,
        selected_herbs=herbs
)

def get_unique_nuts_and_grains():
    """Fetches, splits, and deduplicates nut and grain ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT NutsAndGrains FROM Pantry WHERE NutsAndGrains IS NOT NULL")
    nuts_and_grains_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['NutsAndGrains'].split(',')]
        nuts_and_grains_set.update(parts)
    return sorted(list(nuts_and_grains_set))


@app.route("/nuts-and-grains")
def function9(nuts_and_grains):
    nuts_and_grains = request.args.get("nuts_and_grains", "")

    
    
    nuts_and_grains = get_unique_nuts_and_grains()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if nuts_and_grains:
        
        sql = base_select + " WHERE NutsAndGrains LIKE ?"
        pantry = query_db(sql, (f"%{nuts_and_grains}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        nuts_and_grains=nuts_and_grains,
        selected_nuts_and_grains=nuts_and_grains)

@app.route("/nuts-and-grains/<nuts_and_grains>")
def filter_by_nuts_and_grains(nuts_and_grains):
    nuts_and_grains_items = get_unique_nuts_and_grains()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        nuts_and_grains=nuts_and_grains_items,
        selected_nuts_and_grains=nuts_and_grains
)

def get_unique_miscellaneous():
    """Fetches, splits, and deduplicates miscellaneous ingredients from the DB."""
    raw_data = query_db("SELECT DISTINCT Miscellaneous FROM Pantry WHERE Miscellaneous IS NOT NULL")
    miscellaneous_set = set()
    for row in raw_data:
        
        parts = [p.strip() for p in row['Miscellaneous'].split(',')]
        miscellaneous_set.update(parts)
    return sorted(list(miscellaneous_set))


@app.route("/miscellaneous")
def function10(miscellaneous):
    miscellaneous = request.args.get("miscellaneous", "")

    
    
    miscellaneous = get_unique_miscellaneous()

    
    base_select = """
        SELECT RowNum, Title, Creator, Image, Ingredients, Category, Website 
        FROM (SELECT ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum, 
              Title, Creator, Image, Ingredients, Category, Website 
              FROM Recipes)
    """

    if miscellaneous:
        sql = base_select + " WHERE Miscellaneous LIKE ?"
        pantry = query_db(sql, (f"%{miscellaneous}%",))
    else:
        pantry = query_db(base_select)

    return render_template(
        "home.html", 
        pantry=pantry,
        miscellaneous=miscellaneous,
        selected_miscellaneous=miscellaneous)

@app.route("/miscellaneous/<miscellaneous>")
def filter_by_miscellaneous(miscellaneous):
    miscellaneous_items = get_unique_miscellaneous()
    recipes_data = query_db("SELECT * FROM Recipes")
    return render_template(
        "filtered_recipes.html",
        recipes=recipes_data,
        miscellaneous=miscellaneous_items,
        selected_miscellaneous=miscellaneous
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
        WHERE LOWER(Title) LIKE ? OR LOWER(Ingredients) LIKE ?
        ORDER BY Title ASC;
    """
    like_query = f"%{query}%"
    results = query_db(sql, (like_query, like_query))
    return render_template("search_results.html", results=results, query=query)



@app.route("/recipes/<recipeid>")
def recipe_detail(id):
    return render_template("recipe_detail.html", recipeid=id)
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
        WHERE ID = ?
    """
    recipe = query_db(sql, (id,), one=True)
    if not recipe:
        abort(404)
    return render_template("recipe.html", recipe=recipe)





@app.route("/recipe/id/<id>")
def recipe_by_id(id):
    sql = """
        SELECT Title, Creator, Image, Ingredients, Category, Website, Recipelink
        FROM Recipes
        WHERE ID = ?;
    """
    result = query_db(sql, [id], one=True)
    if result is None:
        return "Recipe not found", 404
    return render_template("recipe.html", recipe=result)


if __name__ == "__main__":
    app.run(debug=True, port=4000, host="0.0.0.0")



