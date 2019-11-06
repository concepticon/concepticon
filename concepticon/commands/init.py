"""

"""
import pathlib
import subprocess
import contextlib

from clldutils import db
import transaction
from pyramid.paster import get_appsettings, bootstrap
from sqlalchemy import engine_from_config
from clld.db.meta import DBSession, Base
from clld.scripts.util import ExistingConfig

import concepticon
from concepticon.scripts.initializedb import prime_cache, main

PROJECT_DIR = pathlib.Path(concepticon.__file__).parent.parent


def register(parser):
    parser.add_argument(
        "--config-uri",
        action=ExistingConfig,
        help="ini file providing app config",
        default=str(PROJECT_DIR / 'development.ini'))
    parser.add_argument(
        '--doi',
        default=None,
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--prime-cache-only',
        action='store_true',
        default=False,
    )


# FIXME: The Session class should go into clld/scripts/util!
class Session:
    def __init__(self, settings):
        self.settings = settings
        self.engine = None

    def __enter__(self):
        self.engine = engine_from_config(self.settings)
        DBSession.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
        return DBSession

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.dispose()


@contextlib.contextmanager
def dryrun_ini(db_):
    p = PROJECT_DIR / 'dryrun.ini'
    p.write_text("""\
[app: main]
use = egg:concepticon
sqlalchemy.url = {0}

[server: main]
use = egg:waitress
host = 0.0.0.0
port = 6543
""".format(db_), encoding='utf8')
    yield p
    p.unlink()


def run(args):
    # FIXME: there should be a clld.scripts.util.bootstrap which does both of:
    args.env = bootstrap(args.config_uri)
    settings = get_appsettings(args.config_uri)

    if args.dry_run:
        settings[db.DB.settings_key] += '.dryrun'
        db_cls = db.TempDB
    else:
        db_cls = db.FreshDB

    with db_cls.from_settings(settings, log=args.log) as db_:
        with Session(settings):
            if not args.prime_cache_only:
                with transaction.manager:
                    main(args)
            with transaction.manager:
                prime_cache(args)
        if args.dry_run:
            with dryrun_ini(db_) as config:
                subprocess.check_call(['pytest', '--appini', str(config)], cwd=str(PROJECT_DIR))
