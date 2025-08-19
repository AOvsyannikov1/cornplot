import os

from .console_plots import *
from .dashboard import Dashboard
from .axles import Axles
try:
    from .railway_dashboard import RailwayDashboard
except ImportError:
    pass
from .filters import *
from .tests import *
from .animation_tests import *
from .utils import UPPER_INDEXES, LOWER_INDEXES

def _get_hook_dirs():
    """Возвращает пути к директориям с хуками PyInstaller"""
    return [os.path.join(os.path.dirname(__file__), 'hooks')]