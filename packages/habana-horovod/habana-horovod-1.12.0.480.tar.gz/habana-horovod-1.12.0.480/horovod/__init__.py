import os
from horovod.runner import run

__version_upstream__ = '0.27.0'


def _get_pkg_version(pkg_info_path):
    with open(pkg_info_path) as f:
        for line in f:
            if line.startswith('Version: '):
                return line.split()[-1].strip()


def _get_version():
    pkg_info_path = os.path.join(os.path.dirname(__file__), '..', 'PKG-INFO')
    if os.path.exists(pkg_info_path):
        try:
            return _get_pkg_version(pkg_info_path)
        except:
            pass

    version = os.getenv('release_version', default="0.0.0")
    build_number = os.getenv('rel_id', default="dev0")
    return ".".join([version, build_number])


# habana-horovod version
__version__ = _get_version()
