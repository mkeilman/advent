import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Foyer:
    def __init__(self, size, robots):
        self.size = size
        self.robots = robots
        self.quadrants = (
            (range(0, self.size[0] // 2), range(0, self.size[1] // 2)),
            (range(self.size[0] // 2 + 1, self.size[0]), range(0, self.size[1] // 2)),
            (range(0, self.size[0] // 2), range(self.size[1] // 2 + 1, self.size[1])),
            (range(self.size[0] // 2 + 1, self.size[0]), range(self.size[1] // 2 + 1, self.size[1])),
        )

    def move_robots(self, num_steps=1):
        for r in self.robots:
            for i in (0, 1):
                r.pos[i] = ((r.pos[i] + num_steps * r.velocity[i]) + self.size[i]) % self.size[i]

    def robot_counts(self):
        c = []
        for q in self.quadrants:
            n = 0
            for r in self.robots:
                if r.pos[0] in q[0] and r.pos[1] in q[1]:
                    n += 1
            c.append(n)
        return c
    
    def safety_factor(self):
        return mathutils.product(self.robot_counts())


class Robot:
    def __init__(self, txt):
        m = re.match(r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)", txt)
        self.init_pos = [int(m.group(1)), int(m.group(2))]
        self.pos = self.init_pos
        self.velocity = (int(m.group(3)), int(m.group(4)))


class AdventDay(Day.Base):

    TEST = [
        "p=0,4 v=3,-3",
        "p=6,3 v=-1,-3",
        "p=10,3 v=-1,2",
        "p=2,0 v=2,-1",
        "p=0,0 v=1,3",
        "p=3,0 v=-2,-2",
        "p=7,6 v=-1,-3",
        "p=3,0 v=-1,-2",
        "p=9,3 v=2,3",
        "p=7,3 v=-1,2",
        "p=2,4 v=2,-3",
        "p=9,5 v=-3,-3",
    ]

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2024,
            14,
            AdventDay.TEST
        )
        self.args_parser.add_argument(
            "--width",
            type=int,
            help="foyer width",
            default=11,
            dest="width",
        )
        self.args_parser.add_argument(
            "--height",
            type=int,
            help="foyer height",
            default=7,
            dest="height",
        )
        self.width = self.args_parser.parse_args(run_args).width
        self.height = self.args_parser.parse_args(run_args).height

    def run(self, v):
        r = [Robot(x) for x in v]
        f = Foyer((self.width, self.height), r)
        #debug(f"R 10 POS {r[10].pos}")
        f.move_robots(num_steps=100)
        #debug(f"R 10 POS {r[10].pos}")
        #debug(f"POS {[x.pos for x in r]}")
        #debug(f"Q {f.quadrants}")
        debug(f"Q C {f.robot_counts()} SAFETY {f.safety_factor()}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
