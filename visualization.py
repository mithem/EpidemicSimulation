from manimlib.imports import *
import pickle


with open("iteration_states.pickle", "rb") as f:
    data = pickle.load(f)


example = {0: {(0, 0): 'normal', (0, 1): 'infected', (0, 2): 'infected', (1, 0): 'normal', (1, 1): 'normal', (1, 2): 'normal', (2, 0): 'infected', (2, 1): 'infected', (2, 2): 'normal'}, 1: {(0, 0): 'normal', (0, 1): 'infected', (0, 2): 'infected', (1, 0): 'normal', (1, 1): 'normal', (1, 2): 'normal', (2, 0): 'infected', (2, 1): 'infected', (2, 2): 'normal'}, 2: {(0, 0): 'normal', (0, 1): 'infected', (0, 2): 'infected', (1, 0): 'normal', (1, 1)
                : 'normal', (1, 2): 'normal', (2, 0): 'infected', (2, 1): 'infected', (2, 2): 'normal'}, 3: {(0, 0): 'normal', (0, 1): 'infected', (0, 2): 'infected', (1, 0): 'normal', (1, 1): 'normal', (1, 2): 'normal', (2, 0): 'infected', (2, 1): 'infected', (2, 2): 'normal'}, 4: {(0, 0): 'normal', (0, 1): 'infected', (0, 2): 'infected', (1, 0): 'normal', (1, 1): 'normal', (1, 2): 'normal', (2, 0): 'infected', (2, 1): 'infected', (2, 2): 'normal'}}


class GridVisualization(Scene):
    CONFIG = {
        "plane_config": {
            "line_frequency": 0.01
        },
        "zoom_factor": 0.05,
        "x_min": 0,
        "x_max": 12,
        "y_min": 0,
        "y_max": 12
    }

    def construct(self):
        def get_color(person: str):
            if person == "normal":
                return BLUE
            if person == "recovered":
                return GREEN
            if person == "infected":
                return RED
            return GREY

        def draw_iteration(iteration):
            self.clear()
            for x in range(x_length + 1):
                for y in range(x_length + 1):
                    self.add(Dot(np.array([x / (x_length / 12) - 6, y / (x_length / 6) - 3, 0]),
                                 color=get_color(iteration[(x, y)])))
        x_length = 0
        for coord in data[0].keys():
            if x_length < coord[0]:
                x_length = coord[0]
        try:
            for i, iteration in data.items():
                draw_iteration(iteration)
                print("Iteration: " + str(i))
                self.wait(0.1)
        except KeyboardInterrupt:
            raise EndSceneEarlyException("hello")
