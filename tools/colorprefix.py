import argparse
import signal
import sys

import click


def main(color: str, prefix: str) -> int:
    prefix = click.style(prefix, fg=color)

    # Ignore keyboard interrupts, forward to parent process.
    signal.signal(signal.SIGINT, lambda sig, frame: None)

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        print(prefix, line, end="")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("color")
    parser.add_argument("prefix")
    args = parser.parse_args()
    sys.exit(main(color=args.color, prefix=args.prefix))
