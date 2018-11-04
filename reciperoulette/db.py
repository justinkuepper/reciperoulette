import sqlite3

from bs4 import BeautifulSoup
import requests

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Refactor this to be random...
def seed_db():
    db = get_db()

    recipes = [
        "https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/",
        "https://www.allrecipes.com/recipe/9023/baked-teriyaki-chicken/",
        "https://www.allrecipes.com/recipe/11758/baked-ziti-i/",
        "https://www.allrecipes.com/recipe/9023/baked-teriyaki-chicken/",
        "https://www.allrecipes.com/recipe/70343/slow-cooker-chicken-taco-soup/",
        "https://www.allrecipes.com/recipe/8669/chicken-cordon-bleu-ii/",
        "https://www.allrecipes.com/recipe/65896/zesty-slow-cooker-chicken-barbecue/",
        "https://www.allrecipes.com/recipe/8887/chicken-marsala/",
        "https://www.allrecipes.com/recipe/12720/grilled-salmon-i/",
        "https://www.allrecipes.com/recipe/141678/slow-cooker-pulled-pork/",
        "https://www.allrecipes.com/recipe/8694/chicken-enchiladas-ii/",
        "https://www.allrecipes.com/recipe/14469/jamies-cranberry-spinach-salad/",
        "https://www.allrecipes.com/recipe/21261/yummy-sweet-potato-casserole/",
        "https://www.allrecipes.com/recipe/24087/restaurant-style-buffalo-chicken-wings/",
        "https://www.allrecipes.com/recipe/12009/creamy-cajun-chicken-pasta/",
        "https://www.allrecipes.com/recipe/14276/strawberry-spinach-salad-i/",
        "https://www.allrecipes.com/recipe/17991/stuffed-green-peppers-i/",
        "https://www.allrecipes.com/recipe/223042/chicken-parmesan/",
        "https://www.allrecipes.com/recipe/11729/american-lasagna/",
        "https://www.allrecipes.com/recipe/13436/italian-sausage-soup-with-tortellini/",
        "https://www.allrecipes.com/recipe/13218/absolutely-ultimate-potato-soup/",
        "https://www.allrecipes.com/recipe/13333/jamies-minestrone/",
        "https://www.allrecipes.com/recipe/13464/homestyle-turkey-the-michigander-way/",
        "https://www.allrecipes.com/recipe/22302/cha-chas-white-chicken-chili/",
        "https://www.allrecipes.com/recipe/16098/alysons-broccoli-salad/",
        "https://www.allrecipes.com/recipe/34613/roquefort-pear-salad/",
        "https://www.allrecipes.com/recipe/222002/chef-johns-stuffed-peppers/",
        "https://www.allrecipes.com/recipe/16409/spinach-and-strawberry-salad/",
        "https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/",
        "https://www.allrecipes.com/recipe/220854/chef-johns-italian-meatballs/"
    ]

    for recipe in recipes:
        page_link = recipe
        page_response = requests.get(page_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        title = page_content.find('h1').get_text()
        image = page_content.find('img', { 'class': 'rec-photo' })
        db.execute('INSERT INTO recipe (title, image_url, link) VALUES (?, ?, ?)', (title, image['src'], page_link))
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    seed_db()
    click.echo('Seeded the database.')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
