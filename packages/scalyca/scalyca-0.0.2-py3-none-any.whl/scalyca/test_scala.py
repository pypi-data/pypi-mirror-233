#!/usr/bin/env python

from scalyca import Scala
from scalyca import colour as c


class ScalaShowcase(Scala):
    app_name = "SCALA showcase"
    description = "./test_scala.py"

    def add_arguments(self):
        self.argparser.add_argument('string', type=str, choices=['foo', 'bar', 'baz'])
        self.argparser.add_argument('number', type=int)

    def main(self):
        print(f"SCALA showcase running: cat '{c.param(self.args.string)}' has {c.param(self.args.number)} kittens")


ScalaShowcase().run()
