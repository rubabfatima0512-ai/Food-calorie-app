"""Module 4 & 5: Calorie Estimation + Nutritional Information Modules.
Looks up the recognized food in the SQLite nutrition database and
scales the values by the user's portion-size multiplier.
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nutrition.db")


def get_nutrition(food_name, portions=1.0):
    """Return nutrition dict for a food, scaled by portion count.

    Returns None if the food is not in the database.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "nutrition.db not found. Run: python3 setup_database.py"
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM foods WHERE name = ?", (food_name,)
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return {
        "name": row["name"].replace("_", " ").title(),
        "serving": row["serving"],
        "portions": portions,
        "calories": round(row["calories"] * portions, 1),
        "protein_g": round(row["protein_g"] * portions, 1),
        "carbs_g": round(row["carbs_g"] * portions, 1),
        "fat_g": round(row["fat_g"] * portions, 1),
    }


def pretty_name(food_name):
    return food_name.replace("_", " ").title()
