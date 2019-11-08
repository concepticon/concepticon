import pathlib

from clld.web.assets import environment

import concepticon


environment.append_path(
    str(pathlib.Path(concepticon.__file__).parent.joinpath('static')),
    url='/concepticon:static/')
environment.load_path = list(reversed(environment.load_path))
