from blink1.blink1 import Blink1


class Blinker():

    def __init__(self):
        self.occupied = False
        self.blink = Blink1()
        self.blink.write_pattern_line(100, 'yellow', 1)
        self.blink.write_pattern_line(100, 'black', 2)

    def set_waiting(self):
        self.blink.play(1,2,0)

    def set_occupied(self, occupied=True):

        self.occupied = occupied
        if self.occupied:
            self.blink.fade_to_color(10, 'red')
        else:
            self.blink.fade_to_color(10, 'green')

    def restore(self):
        self.set_occupied(self.occupied)
