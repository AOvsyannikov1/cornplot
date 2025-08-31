import os
from .console_plots import *
from .dashboard import Dashboard
from .polar_dashboard import DashboardPolar
from .axles import Axles
from .polar_axles import PolarAxles
from .bar_chart import BarChart
try:
    from .railway_dashboard import RailwayDashboard
except ImportError:
    pass
from .filters import *
from .tests import *
from .plot_updater import PlotUpdater
from .utils import UPPER_INDEXES, LOWER_INDEXES, get_upper_index


def _get_hook_dirs():
    """Возвращает пути к директориям с хуками PyInstaller"""
    return [os.path.join(os.path.dirname(__file__), 'hooks')]
