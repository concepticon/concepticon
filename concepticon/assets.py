from clld.web.assets import environment
from clldutils.path import Path

import concepticon


environment.append_path(
    Path(concepticon.__file__).parent.joinpath('static').as_posix(),
    url='/concepticon:static/')
environment.load_path = list(reversed(environment.load_path))
