from flask import Blueprint
from .shared import ApiRoutes as AR, Methods as M
from .queries import recipe, review, ingredient, recipe_action, user, ingredient_in_recipe, photo

routes = Blueprint('api_routes', __name__)


routes.route(AR.REVIEW_CREATE_REVIEW, methods=[M.POST])(review.create_review)
routes.route(AR.REVIEW_DELETE_REVIEW, methods = [M.POST])(review.delete_review)
routes.route(AR.REVIEW_GET_BY_ID, methods = [M.GET])(review.get_review_by_id)
routes.route(AR.REVIEW_GET_BY_RECIPE_ID, methods = [M.GET])(review.get_review_by_recipe_id)

routes.route(AR.RECIPE_ACTION_CREATE, methods = [M.POST])(recipe_action.recipe_action_create)
routes.route(AR.RECIPE_ACTION_DELETE, methods = [M.POST])(recipe_action.recipe_action_delete)
routes.route(AR.RECIPE_ACTION_LIKE, methods = [M.POST])(recipe_action.recipe_action_like)
routes.route(AR.RECIPE_ACTION_UNLIKE, methods = [M.POST])(recipe_action.recipe_action_unlike)
routes.route(AR.RECIPE_ACTION_FAVORITE, methods = [M.POST])(recipe_action.recipe_action_favorite)
routes.route(AR.RECIPE_ACTION_COOK, methods = [M.POST])(recipe_action.recipe_action_cook)

routes.route(AR.GET_RECIPE_ACTIONS , methods = [M.GET])(recipe_action.get_created_actions)
routes.route(AR.RECIPE_ACTION_GET_COOK, methods = [M.GET])(recipe_action.get_recipes_cooked)
routes.route(AR.RECIPE_ACTION_GET_CREATE, methods = [M.GET])(recipe_action.get_recipes_created)
routes.route(AR.RECIPE_ACTION_GET_FAVORITE, methods = [M.GET])(recipe_action.get_recipes_favorited)

routes.route(AR.RECIPE_FILTER, methods = [M.GET, M.POST])(recipe.filter_recipe)
# routes.route(AR.RECIPE_CREATE, methods = [M.GET, M.POST])(recipe.create_recipe)  # indirectly accessed through recipe_action/create

routes.route(AR.INGREDIENT_FILTER, methods = [M.GET, M.POST])(ingredient.filter_ingredient)
routes.route(AR.INGREDIENT_CREATE, methods = [M.GET, M.POST])(ingredient.create_ingredient)

routes.route(AR.INGREDIENT_IN_RECIPE_FILTER, methods = [M.GET, M.POST])(ingredient_in_recipe.filter_ingredient_in_recipe)
routes.route(AR.INGREDIENT_IN_RECIPE_CREATE, methods = [M.GET, M.POST])(ingredient_in_recipe.create_ingredient_in_recipe)
routes.route(AR.INGREDIENT_IN_RECIPE_DELETE, methods = [M.GET, M.POST])(ingredient_in_recipe.delete_ingredient_in_recipe)

routes.route(AR.USER_CREATE_USER, methods=[M.POST])(user.create_user)

routes.route(AR.PHOTO_CREATE_PHOTO, methods=[M.POST])(photo.create_photo)

