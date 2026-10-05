"""Build the SQLite nutrition database for all 101 Food-101 classes.
Values are estimates per typical single serving (calories, protein/carbs/fat in grams).
Run: python3 setup_database.py
"""
import sqlite3
import os

# (food_name, serving description, calories, protein_g, carbs_g, fat_g)
NUTRITION_DATA = [
    ("apple_pie", "1 slice (125g)", 296, 2.4, 42, 13),
    ("baby_back_ribs", "1/2 rack (250g)", 700, 55, 5, 50),
    ("baklava", "1 piece (60g)", 230, 4, 25, 13),
    ("beef_carpaccio", "1 serving (100g)", 150, 20, 2, 7),
    ("beef_tartare", "1 serving (150g)", 280, 25, 3, 18),
    ("beet_salad", "1 cup (150g)", 120, 3, 15, 6),
    ("beignets", "2 pieces (90g)", 320, 5, 45, 13),
    ("bibimbap", "1 bowl (400g)", 550, 25, 70, 18),
    ("bread_pudding", "1 cup (150g)", 340, 8, 50, 12),
    ("breakfast_burrito", "1 burrito (300g)", 600, 28, 55, 30),
    ("bruschetta", "2 pieces (80g)", 150, 4, 22, 5),
    ("caesar_salad", "1 bowl (200g)", 350, 12, 12, 28),
    ("cannoli", "1 piece (90g)", 280, 6, 30, 15),
    ("caprese_salad", "1 serving (150g)", 220, 10, 6, 16),
    ("carrot_cake", "1 slice (100g)", 410, 5, 55, 20),
    ("ceviche", "1 serving (150g)", 150, 25, 8, 2),
    ("cheesecake", "1 slice (100g)", 400, 7, 30, 28),
    ("cheese_plate", "1 serving (100g)", 380, 22, 3, 30),
    ("chicken_curry", "1 cup (250g)", 350, 28, 12, 20),
    ("chicken_quesadilla", "1 quesadilla (200g)", 520, 32, 40, 26),
    ("chicken_wings", "6 pieces (200g)", 480, 36, 4, 34),
    ("chocolate_cake", "1 slice (100g)", 420, 5, 55, 22),
    ("chocolate_mousse", "1 cup (120g)", 350, 5, 28, 25),
    ("churros", "3 pieces (90g)", 340, 4, 42, 18),
    ("clam_chowder", "1 cup (250g)", 250, 12, 20, 14),
    ("club_sandwich", "1 sandwich (280g)", 600, 35, 45, 30),
    ("crab_cakes", "2 pieces (150g)", 320, 24, 12, 18),
    ("creme_brulee", "1 ramekin (120g)", 380, 6, 28, 28),
    ("croque_madame", "1 serving (220g)", 650, 32, 35, 40),
    ("cup_cakes", "1 piece (70g)", 280, 3, 38, 13),
    ("deviled_eggs", "3 pieces (90g)", 200, 9, 2, 17),
    ("donuts", "1 piece (60g)", 300, 4, 35, 16),
    ("dumplings", "6 pieces (150g)", 300, 14, 30, 13),
    ("edamame", "1 cup (150g)", 190, 17, 15, 8),
    ("eggs_benedict", "1 serving (250g)", 550, 26, 30, 35),
    ("escargots", "6 pieces (90g)", 180, 16, 4, 10),
    ("falafel", "4 pieces (100g)", 330, 13, 32, 18),
    ("filet_mignon", "1 steak (200g)", 450, 50, 0, 26),
    ("fish_and_chips", "1 serving (350g)", 800, 35, 70, 40),
    ("foie_gras", "1 serving (50g)", 230, 6, 2, 22),
    ("french_fries", "1 medium serving (120g)", 380, 4, 48, 19),
    ("french_onion_soup", "1 bowl (250g)", 300, 12, 25, 16),
    ("french_toast", "2 slices (150g)", 350, 10, 45, 14),
    ("fried_calamari", "1 serving (150g)", 400, 22, 25, 22),
    ("fried_rice", "1 cup (200g)", 330, 8, 55, 10),
    ("frozen_yogurt", "1 cup (150g)", 220, 6, 40, 4),
    ("garlic_bread", "2 slices (80g)", 280, 6, 35, 13),
    ("gnocchi", "1 cup (200g)", 350, 8, 65, 6),
    ("greek_salad", "1 bowl (250g)", 250, 8, 12, 20),
    ("grilled_cheese_sandwich", "1 sandwich (150g)", 450, 16, 35, 28),
    ("grilled_salmon", "1 fillet (150g)", 310, 34, 0, 18),
    ("guacamole", "1/2 cup (120g)", 220, 3, 12, 20),
    ("gyoza", "6 pieces (150g)", 320, 14, 28, 16),
    ("hamburger", "1 burger (220g)", 550, 28, 40, 30),
    ("hot_and_sour_soup", "1 cup (250g)", 120, 8, 12, 5),
    ("hot_dog", "1 piece (120g)", 320, 10, 25, 20),
    ("huevos_rancheros", "1 serving (300g)", 550, 24, 45, 30),
    ("hummus", "1/2 cup (120g)", 210, 6, 14, 15),
    ("ice_cream", "1 cup (150g)", 300, 5, 35, 16),
    ("lasagna", "1 piece (250g)", 550, 30, 40, 30),
    ("lobster_bisque", "1 cup (250g)", 350, 15, 18, 25),
    ("lobster_roll_sandwich", "1 roll (220g)", 450, 28, 35, 20),
    ("macaroni_and_cheese", "1 cup (220g)", 450, 16, 50, 22),
    ("macarons", "3 pieces (45g)", 220, 4, 28, 11),
    ("miso_soup", "1 cup (250g)", 60, 5, 7, 2),
    ("mussels", "1 serving (150g)", 150, 20, 6, 4),
    ("nachos", "1 serving (200g)", 600, 16, 55, 35),
    ("omelette", "3-egg omelette (180g)", 320, 20, 3, 25),
    ("onion_rings", "1 serving (120g)", 400, 5, 40, 25),
    ("oysters", "6 pieces (90g)", 70, 8, 4, 2),
    ("pad_thai", "1 plate (300g)", 550, 20, 65, 22),
    ("paella", "1 plate (300g)", 550, 28, 60, 20),
    ("pancakes", "3 pieces (200g)", 450, 10, 70, 14),
    ("panna_cotta", "1 serving (120g)", 320, 5, 22, 24),
    ("peking_duck", "1 serving (150g)", 450, 28, 5, 35),
    ("pho", "1 bowl (500g)", 450, 30, 55, 10),
    ("pizza", "2 slices (200g)", 540, 22, 60, 22),
    ("pork_chop", "1 chop (200g)", 450, 45, 0, 28),
    ("poutine", "1 serving (250g)", 700, 15, 70, 40),
    ("prime_rib", "1 serving (200g)", 600, 45, 0, 45),
    ("pulled_pork_sandwich", "1 sandwich (250g)", 550, 32, 50, 22),
    ("ramen", "1 bowl (500g)", 550, 25, 65, 18),
    ("ravioli", "1 cup (200g)", 400, 16, 50, 14),
    ("red_velvet_cake", "1 slice (100g)", 420, 5, 55, 21),
    ("risotto", "1 cup (250g)", 400, 10, 60, 12),
    ("samosa", "2 pieces (120g)", 320, 6, 35, 19),
    ("sashimi", "1 serving (150g)", 180, 28, 2, 5),
    ("scallops", "1 serving (150g)", 150, 24, 5, 2),
    ("seaweed_salad", "1 serving (100g)", 80, 3, 12, 3),
    ("shrimp_and_grits", "1 plate (300g)", 500, 25, 50, 20),
    ("spaghetti_bolognese", "1 plate (300g)", 600, 30, 70, 20),
    ("spaghetti_carbonara", "1 plate (300g)", 650, 28, 65, 30),
    ("spring_rolls", "3 pieces (120g)", 280, 8, 30, 14),
    ("steak", "1 steak (200g)", 550, 50, 0, 36),
    ("strawberry_shortcake", "1 serving (120g)", 350, 5, 50, 15),
    ("sushi", "8 pieces (200g)", 350, 18, 50, 6),
    ("tacos", "2 tacos (200g)", 450, 22, 35, 22),
    ("takoyaki", "6 pieces (150g)", 350, 12, 35, 18),
    ("tiramisu", "1 piece (120g)", 380, 7, 35, 24),
    ("tuna_tartare", "1 serving (150g)", 220, 28, 4, 10),
    ("waffles", "2 pieces (150g)", 400, 9, 55, 16),
]

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nutrition.db")

def build():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            serving TEXT NOT NULL,
            calories REAL NOT NULL,
            protein_g REAL NOT NULL,
            carbs_g REAL NOT NULL,
            fat_g REAL NOT NULL
        )
    """)
    cur.executemany(
        "INSERT INTO foods (name, serving, calories, protein_g, carbs_g, fat_g) VALUES (?,?,?,?,?,?)",
        NUTRITION_DATA,
    )
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
    conn.close()
    print(f"nutrition.db created with {count} foods at {DB_PATH}")

if __name__ == "__main__":
    build()
