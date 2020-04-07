import math
import random as random_module
import warnings
from itertools import zip_longest
from time import sleep
from typing import Union

import numpy as np

from episim.utils import *
from episim.vars import person_types, triggers


class Config:
    def __init__(self, capacity=10000, initial_infections=5, start_iteration=0, iterations=1000, infection_distance=1, infection_chance=0.01, random_movement=0.01, random_infection=True, days_infected=10, resistance=0.95, sleep_time=0.0, r0=0.0, use_tabulate=True, person_types_amount: Union[str, list] = [100], verbose=True):
        self.capacity = capacity
        self.initial_infections = initial_infections
        self.start_iteration = start_iteration
        self.iterations = iterations
        self.infection_distance = infection_distance
        self.infection_chance = infection_chance
        self.random_movement = random_movement
        self.coordinate_system_length = math.floor(math.sqrt(self.capacity))
        self.verbose = verbose
        self.random_infection = random_infection
        self.days_infected = days_infected
        self.resistance = resistance
        self.sleep_time = sleep_time
        self.r0 = r0
        self.use_tabulate = use_tabulate
        self.person_types_amount = get_person_types_amount(person_types_amount)

        if r0 != 0.0 and infection_chance != 0.01:
            warnings.warn(
                "R0 and infection_chance (ic) are both specified, ic will be ignored.")

    def __str__(self):
        return f"""Capacity: {self.capacity}
Initial Infections: {self.initial_infections}
Iterations: {self.iterations}
Random infection (initially): {str(self.random_infection)}
Resistance: {str(self.resistance)}
Coordinate system length: {str(self.coordinate_system_length)}
Days infected: {str(self.days_infected)}
Sleep time: {str(self.sleep_time)}
(Force) R0: {str(self.r0)}
Triggers: {str(len(triggers))}
"""


class Person:
    def __init__(self, infected=False, recovered=False):
        self._infected = infected
        self._recovered = recovered
        self._days_infected = 0
        self.r0 = 0
        self.infection_chance = None
        self.infection_distance = None
        self.random_movement = None
        self.days_infected = None

    @property
    def infected(self):
        return self._infected

    @property
    def recovered(self):
        return self._recovered

    @property
    def normal(self):
        return self._days_infected == 0 and not self.recovered and not self.infected

    @infected.setter
    def infected(self, infected: bool):
        self._infected = infected
        if infected:
            self.recovered = False

    @recovered.setter
    def recovered(self, recovered: bool):
        self._recovered = recovered
        if recovered:
            self.infected = False

    @property
    def status(self):
        if self.infected:
            return "infected"
        elif self.recovered:
            return "recovered"
        else:
            return "normal"

    def act(self, max_days_infected):
        if self.days_infected != None:
            max_days_infected = self.days_infected
        if self._days_infected == max_days_infected:
            self.recovered = True
        if self.infected:
            self._days_infected += 1

    def register(self):
        person_types.append(self.__class__)

    def __str__(self):
        return self.status


class World:
    def __init__(self, config: Config):
        """if `random`, random persons will be chosen to be infected from the start. Otherwise, they will spawn in the top left corner. `Random`might choose the same coordinates/person multiple times."""
        global person_types
        self.config = config
        self.iteration = 0
        self.r0 = 0
        self.coordinates: dict[tuple, Person] = {}
        person_types_amount = {}
        person_types = sort_by_class_name(person_types)
        person_types = fill_person_types_to(person_types,
                                            value=self.config.person_types_amount, total_length=self.config.coordinate_system_length**2)
        print("after:", person_types)
        for x in range(self.config.coordinate_system_length):
            for y in range(self.config.coordinate_system_length):
                self.coordinates[(x, y)] = None
        for cls, coord in zip_longest(person_types, self.coordinates.keys(), fillvalue=Person):
            self.coordinates[coord] = cls()
        if config.random_infection:
            infected_coords = []
            for i in range(self.config.initial_infections):
                x = random_module.randint(
                    0, self.config.coordinate_system_length - 1)
                y = random_module.randint(
                    0, self.config.coordinate_system_length - 1)
                self.coordinates[(x, y)].infected = True
        else:
            i = 0
            x = 0
            y = 0
            while i < config.initial_infections:
                self.coordinates[(x, y)].infected = True
                i += 1
                x += 1
                if x == self.config.coordinate_system_length - 1:
                    y += 1
                    x = 0

    @property
    def status(self):
        """return normal, recovered, infected, R0"""
        n = 0
        r = 0
        i = 0
        for p in self.coordinates.values():
            s = p.status
            if s == "normal":
                n += 1
            elif s == "recovered":
                r += 1
            elif s == "infected":
                i += 1
        return n, r, i, self.r0

    def act(self):
        r0 = 0
        for coord, person in self.coordinates.items():
            if person.infected:
                infection_chance, infection_distance, random_movement = get_custom_properties(
                    self.config, person)
                neighbors = get_neighbor_coords(
                    coord, infection_distance + 1 + random_module.random() * random_movement, self.config.coordinate_system_length - 1)
                for nc in neighbors:
                    if coordinate_distance(coord, nc) <= infection_distance:
                        if random_module.random() < infection_chance:
                            self.infect(nc)
                            person.r0 += 1
                r0 += person.r0
            person.act(self.config.days_infected)
        try:
            r0 /= self.status[2]  # n of infected
        except ArithmeticError:
            r0 = 0
        if self.config.r0 != 0.0:
            prev_r0 = self.r0
            average_r0 = np.average([prev_r0, r0])
            self.config.infection_chance += 0.00025 * \
                (self.config.r0 - average_r0)
        self.r0 = r0
        sleep(self.config.sleep_time)

    def infect(self, coord):
        p = self.coordinates[coord]
        if p.recovered:
            if random_module.random() >= self.config.resistance:
                p.infected = True
        elif p.normal:
            p.infected = True

    def simplify(self):
        result = {}
        for coord, person in self.coordinates.items():
            result[coord] = person.status
        return result

    def __str__(self):
        s = "{\n"
        for coordinate, person in self.coordinates.items():
            s += str(coordinate) + ": " + str(person) + ",\n"
        s += "}"
        return s


class Trigger:
    def __init__(self, iteration: int = None, normal: int = None, recovered: int = None, infected: int = None):
        self.iteration = iteration
        self.normal = normal
        self.recovered = recovered
        self.infected = infected

    def test(self, world: World):
        normal, recovered, infected, r0 = world.status
        if self.iteration != None:
            if world.iteration >= self.iteration:
                return True
        if self.normal != None:
            if normal <= self.normal:
                return True
        if self.recovered != None:
            if recovered >= self.recovered:
                return True
        if self.infected != None:
            if infected >= self.infected:
                return True
        return False

    def register(self):
        triggers.append(self)

    def act(self, world):
        """Override this method to get access to the world and manipulate its config parameters."""
        pass


class SimulationEvent(Exception):
    pass
