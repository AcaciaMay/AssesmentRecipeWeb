import sqlite3

title_to_image = {
"Chicken and Leek Pie": "chickenandleek.jpg",
"BBQ Butterflied Lamb": "bbqlamb.jpg",
"Sticky Five Spice Beef": "spicebeef.jpg",
"Roti Chicken Curry": "chickencurry.jpg",
"Oreo Cheesecake Slice": "oreocheesecake.jpg",
"Chocolate Roulade": "chocolateroulade.jpg",
"Easter Cheesecake Cups": "eastercheesecale.jpg",
"Strawberry Tray Cheesecake": "strawberrytray.jpg",
"Chocolate Roulade": "chocolateroulade.jpg",
"Turkish Delight Rocky Road": "turkishchocolate.jpg",
"Peanut Butter Brownies": "peanutbutterbrownies.jpg"
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