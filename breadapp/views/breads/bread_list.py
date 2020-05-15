import sqlite3
from django.shortcuts import render, redirect, reverse
from ..connection import Connection
from breadapp.models import Bread, model_factory

def bread_list(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Bread)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                b.id,
                b.name,
                b.region
            FROM breadapp_bread b
            ORDER BY b.name ASC
            """)

            all_breads = db_cursor.fetchall()

        template = 'breads/bread_list.html'
        context = {
            'all_breads': all_breads
        }

        return render(request, template, context)

    elif request.method == 'POST': 
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO breadapp_bread 
            (
                name, region
            ) 
            VALUES (?, ?)
            """, (form_data["name"], form_data["region"]))

            return redirect(reverse('breadapp:bread_list'))