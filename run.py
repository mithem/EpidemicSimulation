import argparse
import episim
import importlib
import warnings

p = argparse.ArgumentParser()
p.add_argument("--iterations", "-i", type=int, default=500)
p.add_argument("--initial-infections", "-ii", type=int, default=5)
p.add_argument("--capacity", "-c", type=int, default=1000)
p.add_argument("--infection-distance", "-id", type=float, default=1.1)
p.add_argument("--infection-chance", "-ic", type=float, default=0.01)
p.add_argument("--random-movement", "-rm", type=float, default=0.01)
p.add_argument("--trigger", "-t", action="store_true",
               help="try to import the module 'triggers' where you can specify your own triggers")
args = p.parse_args()

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
