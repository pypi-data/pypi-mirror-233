import argparse
import pathlib

from .generators import generate
from .config import Config


if __name__ == '__main__':
    # parse cli args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        type=str
    )
    parser.add_argument(
        'output',
        type=str,
        default='output.jpg'
    )
    parser.add_argument(
        '--width',
        required=False,
        type=int,
        default=512
    )
    parser.add_argument(
        '--height',
        type=int,
        default=128,
        required=False
    )
    args = parser.parse_args()

    # construct config
    conf = Config(
        pathlib.Path(args.input),
        pathlib.Path(args.output),
        int(args.width),
        int(args.height)
    )

    # run app and print result
    print(generate(
        conf.input,
        conf.output,
        conf.width,
        conf.height
    ))
