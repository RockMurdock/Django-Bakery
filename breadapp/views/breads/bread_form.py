import sqlite3
from django.shortcuts import render
from ..connection import Connection
from breadapp.models import Bread, model_factory


def bread_form(request):
    if request.method == 'GET':
        breads = get_breads()
        template = 'breads/bread_form.html'
        context = {
            'all_breads': breads
        }
        return render(request, template, context)

def get_breads():
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

        return db_cursor.fetchall()