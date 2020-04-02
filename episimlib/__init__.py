from episimlib.objects import *
from episimlib.utils import coordinate_distance
from fileloghelper import VarSet
import matplotlib.pyplot as plt


def main():
    config = Config()
    w = World(config)
    vs = VarSet({"iteration": 0, "infected": 5})
    try:
        for i in range(config.iterations):
            w.act()
            vs.set("iteration", i)
            vs.set("infected", w.infected)
            vs.print_variables()
    except KeyboardInterrupt:
        print("okay you impatient thingy")
    except Exception as e:
        print(str(e))
    finally:
        plt.plot(vs.get_history()["infected"])
        plt.show()
