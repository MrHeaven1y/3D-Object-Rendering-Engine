import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from .models import SimulationRun
from .db import SessionLocal
from .engine import SimulationEngine, SimulationError
from sqlalchemy.orm import Session
from sqlalchemy import update
import datetime