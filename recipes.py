import sqlite3

title_to_image = {
"Chicken and Leek Pie": "chickenandleek.jpg",
"BBQ Butterflied Lamb": "bbqlamb.jpg",
"Sticky Five Spice Beef": "spicebeef.jpg",
"Roti Chicken Curry": "chickencurry.jpg",
"Oreo Cheesecake Slice": "oreocheesecake.jpg",
"Chocolate Roulade": "chocolateroulade.jpg",
"Easter Cheesecake Cups": "eastercheesecake.jpg",
"Strawberry Tray Cheesecake": "strawberrytray.jpg",
"Chocolate Roulade": "chocolateroulade.jpg",
"Turkish Delight Rocky Road": "turkishchocolate.jpg",
"Peanut Butter Brownies": "peanutbutterbrownies.jpg",
"Tiramisu": "tiramasu.jpg", 
"Puttanesca Chicken": "puttanesa.jpg",
"Asparagus Omlette": "asparagusomlette",
"Berry Smoothie": "berrysmoothie.jpg",
"Cauliflower Rice and Eggs": "cauliflowerriceandeggs.jpg",
"Cheese and Herb Garlic Bread": "cheeseandherbgarlicbread",
"Chicken and Leek": "chickenandleek.jpg",
"Chicken Wontons": "chickenwonton.jpg",
"Crepes": 'crepes.jpg',
"Deviled Eggs": "deviledeggs",
"Eggs Benedict": "eggsbenedict.jpg",
"Flat Bread Pizzas": "flatbreadpizzas",
"Honey Garlic Chicken": "honeygarlicchicken",
"Perfect Pancakes": "perfectpancakes",
"Pear and Honey Toast": "pearandhoneytoast",
"Pikelets": "pikelets"
}


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

updated = 0
not_found = []


for title, filename in title_to_image.items():
    image_path = f"images/{filename}"
    cursor.execute("""
        UPDATE Recipes
        SET "Image" = ?
        WHERE Title = ?
    """, (image_path, title))
    if cursor.rowcount == 0:
        not_found.append(title)
    else:
        updated += cursor.rowcount


conn.commit()
conn.close()


print(f"✅ Updated {updated} row(s) in 'Recipes' table.")
if not_found:
    print("\n⚠️ These titles were not found in the database:")
    for title in not_found:
        print(f" - {title}")