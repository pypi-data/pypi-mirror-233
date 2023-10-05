import os
import shutil
import sys
import json
from pprint import pformat
from typing import Optional, Tuple, ContextManager, Dict

import argparse
import logging
from contextlib import contextmanager, ExitStack

import flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_restful import Api
from flask_apispec import FlaskApiSpec

from celery import current_app as current_celery_app
from ewoksjob.client.local import pool_context

from .resources.data import DEFAULT_ROOT

try:
    from ewoksweb.serverutils import get_static_root
except ImportError:

    def get_static_root():
        return "static"


try:
    from ewoksweb.serverutils import get_test_config
except ImportError:
    get_test_config = None

from .resources import add_resources
from .resources.json import utils as resource_utils
from .resources.json.tasks import discover_tasks
from .events.websocket import add_events


def create_app(**config) -> Tuple[flask.Flask, Api, FlaskApiSpec]:
    app = flask.Flask(__name__, static_folder=get_static_root(), static_url_path="")
    CORS(app)
    _configure_app(app, **config)
    apidoc = __add_apidoc(app)
    api = _add_api(app, apidoc)
    return app, api, apidoc


def _add_api(app: flask.Flask, apidoc: FlaskApiSpec) -> Api:
    api = Api(app)
    add_resources(api, apidoc)
    return api


def _configure_app(app: flask.Flask, configuration: Optional[str] = None, **config):
    app.config["CORS_HEADERS"] = "Content-Type"
    filename = os.environ.get("EWOKSSERVER_SETTINGS")
    if configuration:
        filename = configuration
    if filename:
        if not os.path.isabs(filename):
            filename = os.path.relpath(filename, app.config.root_path)
        app.config.from_pyfile(filename, silent=False)
    if config:
        config = {k.upper(): v for k, v in config.items() if v is not None}
        app.config.update(config)
    if app.config.get("CELERY"):
        current_celery_app.conf.update(app.config["CELERY"])

    if not filename and not config:
        app.config["EWOKS"] = {
            "handlers": [
                {
                    "class": "ewokscore.events.handlers.Sqlite3EwoksEventHandler",
                    "arguments": [
                        {
                            "name": "uri",
                            "value": "file:ewoks_events.db",
                        }
                    ],
                }
            ]
        }

    _copy_default_resources(app)


def _print_config(app: flask.Flask):
    resourcedir = app.config.get("RESOURCE_DIRECTORY")
    if not resourcedir:
        resourcedir = "."
    print(f"\nRESOURCE DIRECTORY:\n {os.path.abspath(resourcedir)}\n")

    adict = app.config.get("CELERY")
    if adict is None:
        print("\nCELERY:\n Not configured (local workflow execution)\n")
    else:
        print(f"\nCELERY:\n {pformat(adict)}\n")

    adict = app.config.get("EWOKS")
    if adict is None:
        print("\nEWOKS:\n Not configured\n")
    else:
        print(f"\nEWOKS:\n {pformat(adict)}\n")


def _print_serve_message(host: str, port: int) -> None:
    print("\nTo start editing workflows, open this link in a browser:\n")
    print(f"    http://{host}:{port}\n")


def _set_log_level(app: Optional[flask.Flask] = None, log_level=logging.WARNING):
    logging.basicConfig(level=log_level)
    if app is not None:
        app.logger.setLevel(log_level)


def add_socket(app: flask.Flask) -> SocketIO:
    socketio = SocketIO(app, cors_allowed_origins="*")
    add_events(socketio)
    return socketio


def __add_apidoc(app: flask.Flask) -> FlaskApiSpec:
    app.config.update(
        {
            "APISPEC_TITLE": "ewoks",
            # "APISPEC_OAS_VERSION": "3.0.3",
            "APISPEC_SWAGGER_URL": "/swagger/",
            "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",
        }
    )
    return FlaskApiSpec(app)


def _save_apidoc(apidoc: FlaskApiSpec, filename: str) -> None:
    save_spec_dir = os.path.dirname(filename)
    if save_spec_dir:
        os.makedirs(save_spec_dir, exist_ok=True)
    with open(filename, "w") as f:
        json.dump(apidoc.spec.to_dict(), f)


def _run_app(
    app: flask.Flask,
    host: str,
    port: int,
    socketio: Optional[SocketIO] = None,
    init_context: Optional[ContextManager] = None,
) -> None:
    with run_context(app, init_context=init_context):
        if socketio is None:
            app.run(host=host, port=port)
        else:
            socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True)


@contextmanager
def run_context(
    app: flask.Flask,
    init_context: Optional[ContextManager] = None,
    local_pool_options: Optional[Dict] = None,
):
    with ExitStack() as stack:
        ctx = app.app_context()
        stack.enter_context(ctx)
        if app.config.get("CELERY") is None:
            if local_pool_options is None:
                local_pool_options = dict()
            ctx = pool_context(**local_pool_options)
            stack.enter_context(ctx)
        if init_context is not None:
            ctx = init_context(app)
            stack.enter_context(ctx)
        yield


def _rediscover_tasks(app: flask.Flask):
    tasks = discover_tasks(app)
    root_url = resource_utils.root_url(app.config.get("RESOURCE_DIRECTORY"), "tasks")
    for resource in tasks:
        resource_utils.save_resource(root_url, resource["task_identifier"], resource)


def _copy_default_resources(app: flask.Flask):
    resource_dir = app.config.get("RESOURCE_DIRECTORY")

    for resource, resource_ext in {
        "tasks": [".json"],
        "icons": [".png", ".svg"],
        "workflows": [".json"],
    }.items():
        root_url = resource_utils.root_url(resource_dir, resource)
        os.makedirs(root_url, exist_ok=True)
        for filename in os.listdir(DEFAULT_ROOT / resource):
            _, ext = os.path.splitext(filename)
            if ext not in resource_ext:
                continue

            src = DEFAULT_ROOT / resource / filename
            if not os.path.isfile(src):
                continue

            dest = root_url / filename
            if not os.path.exists(dest):
                shutil.copy(src, dest)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description="REST API for Ewoks")
    parser.add_argument(
        "-l",
        "--log",
        dest="log_level",
        type=str.upper,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument(
        "--host",
        dest="host",
        type=str,
        default="127.0.0.1",
        help="Host name",
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=5000,
        help="Port number",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="configuration",
        type=str,
        default=None,
        help="Path to a python script (equivalent to the environment variable 'EWOKSSERVER_SETTINGS')",
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="resource_directory",
        type=str,
        default=None,
        help="Root directory for resources (e.g. workflows, tasks, icons descriptions)",
    )
    parser.add_argument(
        "-s",
        "--spec-filename",
        dest="spec_filename",
        type=str,
        help="Save the Swagger docs as JSON",
    )
    parser.add_argument(
        "--without-events",
        action="store_true",
        help="Without websocket events",
    )
    parser.add_argument(
        "--frontend-tests",
        action="store_true",
        help="Load frontend test configuration",
    )
    parser.add_argument(
        "-r",
        "--rediscover-tasks",
        action="store_true",
        help="Run task discovery on start up",
    )

    args = parser.parse_args(argv[1:])
    log_level = getattr(logging, args.log_level)

    if args.frontend_tests:
        if get_test_config is None:
            raise RuntimeError("ewoksweb is not installed")
        args.configuration = get_test_config()

    app, _, apidoc = create_app(
        configuration=args.configuration, resource_directory=args.resource_directory
    )
    if args.spec_filename:
        _save_apidoc(apidoc, args.spec_filename)
        return

    if args.without_events:
        socketio = None
    else:
        socketio = add_socket(app)
    _set_log_level(log_level=log_level)

    @contextmanager
    def init_context(app):
        if args.rediscover_tasks:
            _rediscover_tasks(app)
        yield

    _print_config(app)
    _print_serve_message(args.host, args.port)
    _run_app(app, args.host, args.port, socketio=socketio, init_context=init_context)


if __name__ == "__main__":
    sys.exit(main())
