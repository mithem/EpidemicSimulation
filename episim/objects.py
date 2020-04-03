import math
import random as random_module
from episim.utils import coordinate_distance, get_neighbor_coords


class Config:
    def __init__(self, capacity=10000, initial_infections=5, iterations=1000, infection_distance=1, infection_chance=0.01, random_movement=0.01, random_infection=True, verbose=True):
        self.capacity = capacity
        self.initial_infections = initial_infections
        self.iterations = iterations
        self.infection_distance = infection_distance
        self.infection_chance = infection_chance
        self.random_movement = random_movement
        self.coordinate_system_length = math.floor(math.sqrt(self.capacity))
        self.verbose = verbose
        self.random_infection = random_infection

    def __str__(self):
        return f"Capacity: {self.capacity}\nInitial Infections: {self.initial_infections}\nIterations: {self.iterations}\nInfection Distance: {self.infection_distance}\nInfection chance: {self.infection_chance}\nRandom infection (initially): {str(self.random_infection)}"


class Person:
    def __init__(self, infected=False, recovered=False):
        self._infected = infected
        self._recovered = recovered

    @property
    def infected(self):
        return self._infected

    @property
    def recovered(self):
        return self._recovered

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

    def __str__(self):
        return self.status


class World:
    def __init__(self, config: Config):
        """if `random`, random persons will be chosen to be infected from the start. Otherwise, they will spawn in the top left corner. `Random`might choose the same coordinates/person multiple times."""
        self.config = config
        self.iteration = 0
        self.coordinates: dict[tuple, Person] = {}
        for x in range(self.config.coordinate_system_length):
            for y in range(self.config.coordinate_system_length):
                self.coordinates[(x, y)] = Person()
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
            while i < infected:
                self.coordinates[(x, y)].infected = True
                i += 1
                x += 1
                if x == self.config.coordinate_system_length - 1:
                    y += 1
                    x = 0

    @property
    def infected(self):
        i = 0
        for p in self.coordinates.values():
            if p.infected:
                i += 1
        return i

    def act(self):
        for coord, person in self.coordinates.items():
            neighbors = get_neighbor_coords(
                coord, self.config.infection_distance + 1, self.config.coordinate_system_length - 1)
            for nc in neighbors:
                if (coordinate_distance(coord, nc) <= self.config.infection_distance and (person.infected or self.coordinates[nc].infected) and random_module.random() < self.config.infection_chance) or random_module.random() < self.config.random_movement * 0.0001:
                    person.infected = True
                    self.coordinates[nc].infected = True

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
