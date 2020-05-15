import sqlite3
from django.shortcuts import render, redirect
from breadapp.models import Bread, Ingredient, model_factory
from django.urls import reverse
from ..connection import Connection

def get_breads(bread_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Bread)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            b.id,
            b.name,
            b.region
        FROM breadapp_bread b
        WHERE b.id = ?;
        """, (bread_id,))

        return db_cursor.fetchone()

def create_ingredient(cursor, row):
    row = sqlite3.Row(cursor, row)

    ingredient = Ingredient()
    ingredient.bread_ingredient_id = row["id"]
    ingredient.name = row["name"]
    ingredient.amount = row["amount"]

    return(ingredient)

def get_bread_ingredients(bread_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_ingredient
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            bi.id,
            bi.amount,
            i.name
        FROM breadapp_ingredient i
        JOIN breadapp_breadingredient bi ON bi.ingredient_id = i.id
        WHERE bi.bread_id = ?;
        """, (bread_id,))

        return db_cursor.fetchall()

def bread_details(request, bread_id):
    if request.method == 'GET':
        bread = get_breads(bread_id)
        ingredients = get_bread_ingredients(bread_id)

        template = 'breads/bread_details.html'
        context = {
            'bread': bread,
            'ingredients':ingredients
        }

        return render(request, template, context)
