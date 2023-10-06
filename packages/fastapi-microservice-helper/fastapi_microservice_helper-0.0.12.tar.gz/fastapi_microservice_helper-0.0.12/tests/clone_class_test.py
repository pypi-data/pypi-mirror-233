import os
import sys


app_dir = os.path.abspath(os.path.dirname(__file__)) + '/..'
if app_dir not in sys.path:
    sys.path.append(app_dir)

from src.fastapi_microservice_helper.clone_generation import CloneGeneration
from tests.dto import UpdateUserDto, LocationDto

clone_class = CloneGeneration()

print(clone_class.clone_class_to_dataclass(UpdateUserDto))
print(clone_class.clone_class_to_dataclass(LocationDto))
