# Recipe Roulette

Recipe Roulette is an evolving experiment in applying machine learning to meal planning.

## Getting Started

Recipe Roulette is a Flask application tested against Python `>= 3.6`.

To install Recipe Roulette, clone this repo and run:

`pip install -e .`

After you install the package, initialize and seed the database:

`flask init-db`

The script will automatically import ~20 recipes.

## Use

Users can sign up and rate recipes based on the title, image, and link.

As ratings accumulate, recommendations will begin to appear under the recipe to rate.

## Configuration

You can configure multiple forms of machine learning by passing a different argument into the `getRecommendations` function in the `rating.py` blueprint.

The current options are:
* Euclidean Distance: `similarity=sim_distance`
* Pearson Coefficient: `similarity=sim_pearson`

## What's Next?

This project will be live on its own domain in the near-term.

The long-term goal is to experiment with other forms of machine learning and eventually evolve the app into a more full-fledged meal planner that optimizes for taste and nutrition.

## Contributors & Legalese

If you're interested in contributing, please open a pull request and I'm happy to review it!

Recipe Roulette is copyright (C) 2018 Justin Kuepper. It's licensed under the MIT License.
