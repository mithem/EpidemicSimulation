import episim


class MyTrig(episim.Trigger):
    def act(self, world: episim.World):
        world.config.infection_chance = 0.01


class AnotherTrig(episim.Trigger):
    def act(self, world: episim.World):
        world.config.infection_chance = 0.02


triggers = [MyTrig(infected=100), AnotherTrig(100)]
