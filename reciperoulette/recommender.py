from math import sqrt
import os

from reciperoulette.db import get_db

# Euclidian Distance Score
def sim_distance(p1, p2):
    db = get_db()
    p1reviews = dict(db.execute('SELECT recipe_id, rating FROM rating WHERE user_id = ?', p1).fetchall())
    p2reviews = dict(db.execute('SELECT recipe_id, rating FROM rating WHERE user_id = ?', p2).fetchall())
    si = {}
    for item in p1reviews:
        if item in p2reviews:
            si[item] = 1
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(p1reviews[item] - p2reviews[item], 2) for item in si])
    return 1 / (1 + sqrt(sum_of_squares))

# Pearson Correlation Score
def sim_pearson(p1, p2):
    db = get_db()
    p1reviews = dict(db.execute('SELECT recipe_id, rating FROM rating WHERE user_id = ?', p1).fetchall())
    p2reviews = dict(db.execute('SELECT recipe_id, rating FROM rating WHERE user_id = ?', p2).fetchall())
    si = {}
    for item in p1reviews:
        if item in p2reviews: si[item] = 1
    n = len(si)
    if n == 0: return 0
    sum1 = sum([p1reviews[it] for it in si])
    sum2 = sum([p2reviews[it] for it in si])
    sum1Sq = sum([pow(p1reviews[it], 2) for it in si])
    sum2Sq = sum([pow(p2reviews[it], 2) for it in si])
    pSum = sum([p1reviews[it] * p2reviews[it] for it in si])
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r

# Similarity Algorithm
def topMatches(person, n = 5, similarity = sim_pearson):
    db = get_db()
    users = db.execute('SELECT id FROM user').fetchall()
    user_list = [str(x[0]) for x in users]
    scores = [(similarity(person, other), other) for other in user_list if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Recommendation System
def getRecommendations(person, similarity = sim_pearson):
    db = get_db()
    person = str(person)
    users = db.execute('SELECT id FROM user').fetchall()
    user_list = [str(x[0]) for x in users]
    reviews = dict(db.execute('SELECT recipe_id, rating FROM rating WHERE user_id = ?', person).fetchall())
    totals = {}
    simSums = {}
    for other in user_list:
        if other == person: continue
        sim = similarity(person, other)
        if sim <= 0: continue
        other_reviews = dict(db.execute('SELECT recipe_id, rating FROM rating WHERE user_id = ?', other).fetchall())
        for item in other_reviews:
            if item not in reviews or reviews[item] == 0:
                totals.setdefault(item, 0)
                totals[item] += other_reviews[item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
