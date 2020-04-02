from episim.objects import *
from episim.utils import coordinate_distance, moving_average
from fileloghelper import VarSet
import matplotlib.pyplot as plt


def main(config: Config = None):
    if config == None:
        config = Config()
    w = World(config)
    vs = VarSet({"iteration": 0, "infected": 5, "new_infections": 0, "k": 0})
    try:
        old_infections = 1
        old_infection_n = 1
        print("iteration, infected, new_infections, k")
        for i in range(config.iterations):
            w.act()
            new_infections = w.infected - old_infection_n + 0.0000001
            vs.set("iteration", i)
            vs.set("infected", w.infected)
            vs.set("new_infections", new_infections)
            vs.set("k", float(new_infections) / old_infections)
            vs.print_variables()
            old_infection_n = w.infected
            old_infections = new_infections
    except KeyboardInterrupt:
        print("okay you impatient thingy")
    except Exception as e:
        print(str(e))
    finally:
        history = vs.get_history()
        t = range(config.iterations)
        smooth_news = moving_average(history["new_infections"], 30)

        fig, ax1 = plt.subplots()

        color = "tab:red"

        ax1.set_xlabel("iterations (days)")
        ax1.set_ylabel("total infections", color=color)
        try:
            ax1.plot(t, history["infected"], color=color)
        except ValueError:
            ax1.plot(history["infected"], color=color)
        ax1.tick_params(axis="y", color=color)

        ax2 = ax1.twinx()

        color = "tab:blue"
        ax2.set_ylabel("new infections", color=color)
        try:
            ax2.plot(t, smooth_news, color=color)
        except ValueError:
            ax2.plot(smooth_news, color=color)

        fig.tight_layout()
        plt.show()
