from clld.web.assets import environment
from path import path

import concepticon


environment.append_path(
    path(concepticon.__file__).dirname().joinpath('static'), url='/concepticon:static/')
environment.load_path = list(reversed(environment.load_path))
