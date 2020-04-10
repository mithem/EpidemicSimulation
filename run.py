import argparse
import episim
import importlib
import warnings

c = episim.Config()  # example config for unified default values (Config <-> Argparse(r))

p = argparse.ArgumentParser()
p.add_argument("--iterations", "-i", type=int, default=c.iterations)
p.add_argument("--initial-infections", "-ii",
               type=int, default=c.initial_infections)
p.add_argument("--capacity", "-c", type=int, default=c.capacity)
p.add_argument("--infection-distance", "-id",
               type=float, default=c.infection_distance)
p.add_argument("--infection-chance", "-ic", type=float, default=c.infection_chance,
               help="chance that A infects B when both are in close proximity (infection distance)")
p.add_argument("--random-movement", "-rm", type=float, default=c.random_movement,
               help="a small chance for people to exceed their infection distance and therefore infect even more")
p.add_argument("--no-random-infection", "-nri", action="store_false", dest="random_infection",
               help="specify whether infections should NOT be randomly spread between the coordinates or if they should start in (0, 0)")
p.add_argument("--days-infected", "-di", type=int, default=c.days_infected,
               help="n of days an infected person is counted as infected and is able to infect others")
p.add_argument("--resistance", "-r", type=float, default=c.resistance,
               help="Probability that recovered persons are resistant against another infections")
p.add_argument("-r0", "-R0", "--force-r0", "--force-R0", type=float, default=c.r0, dest="r0",
               help="A value for R0 which will be used to adjust the infection_chance automatically to achieve R0=whatever is specified")
p.add_argument("--use-custom", "--custom", "-uc", action="store_true", dest="use_custom",
               help="try to import the module 'custom' where you can specify your own triggers and person classes")
p.add_argument("--person-amount", "-pa", type=str, dest="person_types_amount", default=c.person_types_amount,
               help="a str like this: '2:1' to mark the relation of different person groups (classes). Requires --use-custom.")
p.add_argument("--sleep-time", "-st", type=int, default=c.sleep_time,
               help="Sleep by this after every iteration")
p.add_argument("--no-tabulate", "-nt", action="store_false", dest="use_tabulate",
               help="Do NOT use tabulate to stream data of the simulation to console. It looks kinda glitchy though as the tables just scroll by..")
p.add_argument("--resistant-days", "-rd", type=int, default=c.resistant_days,
               help="number of days a person is resistant with a chance of --resistant; after this time, the person will be able to be infected again.")
p.add_argument("--verbose", "-v", action="store_true")
args = p.parse_args()

use_custom = args.use_custom
del args.use_custom

if use_custom:
    try:
        import custom
        for a in dir(custom):
            attr = getattr(custom, a)
            if isinstance(attr, (episim.Trigger, episim.Person)):
                attr.register()
    except ImportError:
        warnings.warn(
            "Cannot import module 'triggers'. You should specify your triggers there.")

print(args)
config = episim.Config(**vars(args))


episim.main(config)
