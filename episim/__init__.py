from episim.objects import *
from episim.utils import coordinate_distance, moving_average
from fileloghelper import VarSet
import matplotlib.pyplot as plt
from time import sleep
import json
import pickle


def main(config: Config = None):
    if config == None:
        config = Config()
    if config.verbose:
        print(config)
    world = World(config)
    vs = VarSet({"iteration": 0, "infected": config.initial_infections,
                 "new_infections": 0, "k": 0})
    try:
        iteration_states = {}
        old_infections = 1.0
        old_infection_n = 1.0
        print("iteration, infected, new_infections, k")
        for i in range(config.iterations):
            world.iteration = i
            world.act()
            iteration_states[i] = world.simplify()
            new_infections = world.infected - old_infection_n + 0.0000001
            vs.set("iteration", i)
            vs.set("infected", world.infected)
            vs.set("new_infections", new_infections)
            vs.set("k", float(new_infections) / old_infections)
            vs.print_variables()
            old_infection_n = world.infected
            old_infections = new_infections
            for t in triggers:
                if t.test(world):
                    t.act(world)
                    triggers.pop(triggers.index(t))
    except KeyboardInterrupt:
        print("okay you impatient thingy")
    except Exception as e:
        print(str(e))
        raise e
    finally:
        with open("iteration_states.pickle", "wb") as f:
            f.write(pickle.dumps(iteration_states))
        history = vs.get_history()
        vs.history_to_csv("stats.csv")
        t = list(range(config.iterations + 1))
        smooth_news = [moving_average(history["new_infections"], 5)[i] for i in range(
            29)] + moving_average(history["new_infections"], 30)  # first 30 iterations cannot be calculated

        fig, ax1 = plt.subplots()

        color = "tab:red"

        ax1.set_xlabel("iterations (days)")
        ax1.set_ylabel("total infections", color=color)
        try:
            ax1.plot(t, history["infected"], color=color)
        except ValueError as e:
            print("*"*50)
            print(e)
            print("*"*50)
            ax1.plot(history["infected"], color=color)
        ax1.tick_params(axis="y", color=color)

        ax2 = ax1.twinx()

        color = "tab:blue"
        ax2.set_ylabel("new infections", color=color)
        try:
            ax2.plot(t, smooth_news, color=color)
        except ValueError as e:
            print("*"*50)
            print(e)
            print("*"*50)
            ax2.plot(smooth_news, color=color)

        fig.tight_layout()
        plt.title("Epidemic Simulator!")
        plt.show()


class Trigger:
    def __init__(self, iteration: int = None, infected: int = None):
        self.iteration = iteration
        self.infected = infected

    def test(self, world: World):
        if self.iteration != None:
            if world.iteration >= self.iteration:
                return True
        if self.infected != None:
            if world.infected >= self.infected:
                return True
        return False

    def register(self):
        triggers.append(self)

    def act(self, world):
        """Override this method to get access to the world and manipulate its config parameters."""
        pass


triggers = []
