import os

from API_SearchMovies.config import config_dict
from API_SearchMovies import create_app


get_config_mode = os.environ.get('FLASK_ENV')

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Development, Production, Testing] ')

app = create_app(app_config)
# Migrate(app, db)


if __name__ == '__main__':
    # use_debugger --> to use an external debugger
    # use_reloader --> to stop app from reloading again if false, True will reload if update in app.
    app.run(use_debugger=False, use_reloader=True)
