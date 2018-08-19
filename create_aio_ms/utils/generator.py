from distutils.dir_util import copy_tree
import shutil
import os


from jinja2 import (
    Environment,
    BaseLoader,
)


from create_aio_ms.constants import (
    TEMPLATE_DIR,
    TEMPLATE_NAME,
)
from create_aio_ms.constants import RENDER_ACCESS_FORMATS

__all__ = [
    'copy_template',
    'render_project_template',
    'rename_dirs',
]

render_from_string = Environment(loader=BaseLoader).from_string


def copy_template(dir_name: str) -> None:
    copy_tree(TEMPLATE_DIR, dir_name)


def rename_dirs(dir_name: str) -> None:
    shutil.move(f"{dir_name}/{TEMPLATE_NAME}", f"{dir_name}/{dir_name}")


def render_project_template(context: dict) -> None:
    for root, dors, files in os.walk(f'{context["name"]}'):
        access_files = [
            _file for _file in files
            if _file.split('.')[-1] in RENDER_ACCESS_FORMATS
        ]

        for file_path in access_files:
            with open(f"{root}/{file_path}", 'r+') as my_file:
                body = my_file.read()
                render_body = render_from_string(body).render(**context)
                my_file.seek(0)
                my_file.write(render_body)
                my_file.truncate()