import logging

from rich.logging import RichHandler


def set_log(level="INFO"):
    hand = [RichHandler()]

    logging.basicConfig(level=level, format="%(message)s", handlers=hand)

    logging.debug("Level : %s - %s" % (level, hand))
