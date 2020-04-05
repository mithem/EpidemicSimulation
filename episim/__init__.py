import json
import pickle
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from fileloghelper import VarSet

from episim.objects import *
from episim.utils import coordinate_distance, moving_average


def main(config: Config = None, world: World = None, vs: VarSet = None, iteration_states: dict = {}, old_infection_n=0, old_infections=0):
    if config == None:
        config = Config()
    if config.verbose:
        print(config)
    if world == None:
        world = World(config)
    if vs == None:
        vs = VarSet({"iteration": 0, "infected": config.initial_infections,
                     "new_infections": 0, "k": 0, "normal": config.capacity - config.initial_infections, "recovered": 0, "r0": 0})
    try:
        if config.verbose:
            print(f"Using {str(len(triggers))} triggers.")
        old_infections = 1.0
        old_infection_n = 1.0
        print("iteration, infected, new_infections, k, normal, recovered, r0")
        for i in range(config.start_iteration, config.iterations):
            world.iteration = i
            world.act()
            iteration_states[i] = world.simplify()
            normal, recovered, infected, r0 = world.status
            new_infections = infected - old_infection_n
            vs.set("iteration", list(iteration_states.keys())[-1])
            vs.set("infected", infected)
            vs.set("new_infections", new_infections)
            try:
                vs.set("k", round(float(new_infections / old_infections), 3))
            except ArithmeticError:
                vs.set("k", 0)
            vs.set("normal", normal)
            vs.set("recovered", recovered)
            vs.set("r0", r0)
            vs.print_variables()
            old_infection_n = infected
            old_infections = new_infections
            for t in triggers:
                if t.test(world):
                    t.act(world)
                    triggers.pop(triggers.index(t))
            if infected == 0:
                raise SimulationEvent(
                    "\nNo infected people. Epidemic is over!\n")
        world.iteration += 1
        print(
            f"\n\nFinished simulation! ({str(world.iteration)} iterations)\n")
    except KeyboardInterrupt:
        print("\nokay you impatient thingy\n")
    except Exception as e:
        print(str(e))
        raise e
    except SimulationEvent as e:
        print(str(e))
    finally:
        evalutation(vs, world, iteration_states)
        if input("continue/exit [c/e]?> ").lower() == "c":
            new_iter_max = int(
                input("How many iterations do you want?> "))
            config.start_iteration = world.iteration
            config.iterations = new_iter_max
            config.verbose = False
            main(config, world, vs, iteration_states,
                 old_infection_n, old_infections)


def evalutation(vs: VarSet, world, iteration_states):
    print("Saving data…")
    with open("iteration_states.pickle", "wb") as f:
        f.write(pickle.dumps(iteration_states))
    history = vs.get_history()
    # could be any 'stream' of data
    t = list(range(len(history["recovered"])))
    vs.history_to_csv("stats.csv")
    smooth_news = [moving_average(history["new_infections"], 5)[i] for i in range(
        29)] + moving_average(history["new_infections"], 30)  # first 30 iterations cannot be calculated

    print("Overall (mean) R0: " + str(np.mean(history["r0"])))

    fig, ax1 = plt.subplots()

    color = "tab:red"

    ax1.set_xlabel("iterations (days)")
    ax1.set_ylabel("# of cases")
    try:
        ax1.plot(t, history["infected"], color=color, label="infected")
        ax1.plot(t, history["normal"], color="blue", label="normal")
        ax1.plot(t, history["recovered"], color="green", label="recovered")
    except ValueError as e:
        print("*"*50)
        print(e)
        print("*"*50)
        ax1.plot(history["infected"], color=color)
    ax1.set_title("Absolute cases")
    ax1.legend()
    ax1.tick_params(axis="y", color=color)

    fig2, ax2 = plt.subplots()

    color = "tab:blue"
    ax2.set_ylabel("new infections", color="blue")
    ax2.set_xlabel("iterations (days)")
    ax3 = ax2.twinx()
    try:
        ax2.plot(t, smooth_news, color=color, label="new infections")
        ax3.plot(t, history["r0"], color="orange", label="R0")
    except ValueError as e:
        print("*"*50)
        print(e)
        print("*"*50)
        ax2.plot(smooth_news, color=color, label="new infections")
        ax3.plot(history["r0"], color="orange", label="R0")
    ax3.set_ylabel("R0", color="orange")
    ax2.set_title("New infections, R0")

    fig.tight_layout()
    plt.show()


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


triggers = []
