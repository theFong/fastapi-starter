__version__ = "0.1.0"

from . import database
from . import models

# must be called after all models
database.setup_models()
