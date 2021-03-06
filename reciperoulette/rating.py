from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from reciperoulette.auth import login_required
from reciperoulette.db import get_db

from reciperoulette import recommender

bp = Blueprint('rating', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        rating = request.form['rating']
        recipe_id = request.form['recipe']
        error = None
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO rating (recipe_id, user_id, rating)'
                ' VALUES (?, ?, ?)',
                (recipe_id, g.user['id'], rating)
            )
            db.commit()
            return redirect('/')
    else:
        db = get_db()
        recipe = db.execute(
            'SELECT * FROM recipe r WHERE r.id'
            ' NOT IN (SELECT recipe_id FROM rating WHERE user_id = ?)'
            ' ORDER BY RANDOM() LIMIT 1',
            (g.user['id'],)
        ).fetchone()
        recommendations = recommender.getRecommendations(g.user['id'])
        recommendation_ids = [x[1] for x in recommendations]
        recommendation_ids_sql = tuple(recommendation_ids)
        recommended_recipes = db.execute(
            'SELECT * FROM recipe WHERE id IN {}'.format(recommendation_ids_sql)
        )
        return render_template('rating/index.html', recipe=recipe, recommendations=recommended_recipes)
