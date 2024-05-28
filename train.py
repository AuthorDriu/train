import platform

from argparse import ArgumentParser
from time import time_ns
from os import system


_platform = platform.system()
clear_command = "cls" if _platform == "Windows" else "clear"


class Screen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.heigth = height
        self.train = Train()
    
    def _delay(self, delay):
        time_start = time_ns()
        while time_ns() - time_start < delay:
            pass

    def run(self, delay_ns: int = 100000000, repeats_quantity=0):
        repeation_condition = (lambda x: x < repeats_quantity) if repeats_quantity else (lambda x: True)
        repeats_counter = 0
        direction = 1

        while repeation_condition(repeats_counter):
            screen = ["".rjust(self.width, " ") for _ in range(self.heigth)]
            self.train.move(direction, 0)
            printing = self.train.print(screen)
            
            system(clear_command)
            print(*printing, sep="\n")

            if not self.train.is_visible(screen):
                self.train.is_reversed = not self.train.is_reversed
                direction = -direction
                repeats_counter += 1
            
            self._delay(delay_ns)


class Train:
    image = [
        r"+---------+                ",
        r"|         |        +---+   ",
        r"|         |        |   |   ",
        r"|         +--------+---+--+",
        r"|                         |",
        r"|     __            __    |",
        r"+----/  \----------/  \---+",
        r"     \__/          \__/    "
    ]

    x = -len(image)
    y = 0
    is_reversed = False

    def move(self, delta_x, delta_y):
        """Moves train's coords"""
        self.x += delta_x
        self.y += delta_y
    
    def is_visible(self, screen: list[str]) -> bool:
        """Return true if the train is visible on the screen"""
        for y in range(len(self.image)):
            for x in range(len(self.image[0])):
                real_y = y + self.y
                real_x = x + self.x

                if real_y >= 0 and real_y < len(screen) and \
                    real_x >= 0 and real_x < len(screen[0]):
                    return True
        
        return False

    def get_image(self):
        image = self.image.copy()
        
        if self.is_reversed:
            for i, line in enumerate(image):
                # Явно какая-то фигня, но как есть пока что
                line = line.replace("\\", "!")
                line = line.replace("/", "\\")
                line = line.replace("!", "/")
                image[i] = line[-1::-1]
        
        return image

    def print(self, screen: list[str]) -> list[str]:
        """Prints the train to screen"""
        screen = [list(line) for line in screen]
        image = self.get_image()

        for y in range(len(image)):
            for x in range(len(image[0])):
                real_y = y + self.y
                real_x = x + self.x

                if real_y >= 0 and real_y < len(screen) and \
                    real_x >= 0 and real_x < len(screen[0]):
                    screen[real_y][real_x] = image[y][x]
        
        for i, line in enumerate(screen):
            screen[i] = "".join(line)
        
        return screen


if __name__ == "__main__":
    parser = ArgumentParser("Train", "python3 train.py resolution [options]",
                            "Draws a moving train")
    parser.add_argument("resolution", help="In characters. Example: 80x24, where 80 is width, 24 is height")
    parser.add_argument("-d", "--delay", type=int, default=10000000, help="In nanoseconds")
    parser.add_argument("-r", "--repeats", type=int, default=0, help="Sets repeats quantity. If not set starts infinite loop")
    args = parser.parse_args()

    resolution = args.resolution.split("x")
    xres = int(resolution[0])
    yres = int(resolution[1])

    screen = Screen(xres, yres)
    
    try:
        screen.run(args.delay, args.repeats)
    except KeyboardInterrupt:
        pass
    finally:
        system(clear_command)
        print("Exit program...")
