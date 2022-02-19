from flask import Blueprint

api_id = Blueprint('api_id', __name__,
                   template_folder='templates',
                   static_folder='static')

from API_SearchMovies.Search_byID_api import views
