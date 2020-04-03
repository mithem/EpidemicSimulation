import episim


class MyTrig(episim.Trigger):
    def act(self, world: episim.World):
        world.config.infection_chance = 0.01


class AnotherTrig(episim.Trigger):
    def act(self, world: episim.World):
        world.config.infection_chance = 0.015


triggers = [MyTrig(infected=20), AnotherTrig(100), MyTrig(infected=500)]
