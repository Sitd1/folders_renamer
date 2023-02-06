from renamer import Renamer
from utils import get_config

rn = Renamer(get_config('config.yaml'))
rn.rename()
