import random
RNG = random.Random(42)


class ColorPicker:
    colours = ["darkred", "indianred", "fuchsia", "hotpink", "darkgreen", "chartreuse", "darkblue", "blue",
               "aqua", "darkviolet", "mediumpurple", "dimgrey", "darkorange", "maroon", "yellow", "orange", "teal"]
    basic_colours = ["red", "magenta", "green", "blue", "black", "orange", "maroon", "cyan"]
    RNG.shuffle(colours)

    @staticmethod
    def get_color_given_index(i: int) -> str:
        return ColorPicker.colours[i % len(ColorPicker.colours)]

    @staticmethod
    def get_default_color() -> str:
        return "black"