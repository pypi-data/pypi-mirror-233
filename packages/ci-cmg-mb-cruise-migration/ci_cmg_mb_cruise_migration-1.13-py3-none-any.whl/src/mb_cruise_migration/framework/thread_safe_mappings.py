import copy
import threading

from src.mb_cruise_migration.models.cruise.cruise_mappings import Mapping


class ThreadSafeMappings(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__mappings = []

    def add(self, mapping: tuple):
        with self.__lock:
            self.__mappings.append(mapping)

    def get(self):
        joins = []
        with self.__lock:
            joins = copy.deepcopy(self.__mappings)
        return joins
