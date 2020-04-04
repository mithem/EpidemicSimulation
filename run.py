import argparse
import episim
import importlib
import warnings

p = argparse.ArgumentParser()
p.add_argument("--iterations", "-i", type=int, default=500)
p.add_argument("--initial-infections", "-ii", type=int, default=5)
p.add_argument("--capacity", "-c", type=int, default=1000)
p.add_argument("--infection-distance", "-id", type=float, default=2)
p.add_argument("--infection-chance", "-ic", type=float, default=0.01,
               help="chance that A infects B when both are in close proximity (infection distance)")
p.add_argument("--random-movement", "-rm", type=float, default=0.01,
               help="a small chance for people to exceed their infection distance and therefore infect even more")
p.add_argument("--no-random-infection", "-nri", action="store_true",
               help="specify whether infections should NOT be randomly spread between the coordinates or if they should start in (0, 0)")
p.add_argument("--days-infected", "-di", type=int, default=10,
               help="n of days an infected person is counted as infected and is able to infect others")
p.add_argument("--resistance", "-r", type=float, default=0.95,
               help="Probability that recovered persons are resistant against another infections")
p.add_argument("--trigger", "-t", action="store_true",
               help="try to import the module 'triggers' where you can specify your own triggers")
p.add_argument("--sleep-time", "-st", type=int, default=0.0,
               help="Sleep by this after every iteration")
args = p.parse_args()

nri = args.no_random_infection
del args.no_random_infection
args.random_infection = not nri

trigger = args.trigger
del args.trigger

if trigger:
    try:
        import triggers
        try:
            trigs = [getattr(triggers, "trigger")]
        except AttributeError:
            trigs = getattr(triggers, "triggers")
        for trig in trigs:
            if isinstance(trig, episim.Trigger):
                trig.register()
            else:
                raise TypeError("trigger not of type episim.Trigger.")
    except ImportError:
        warnings.warn(
            "Cannot import module 'triggers'. You should specify your triggers there.")
    except AttributeError:
        warnings.warn(
            "'triggers' module neither has a 'trigger': Trigger attribute, nor 'triggers': [Trigger]")


config = episim.Config(**vars(args))


episim.main(config)
