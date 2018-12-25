from argparse import ArgumentParser
from datetime import datetime

from pixela2img import Pixela2Img


def _parse_argument():
    parser = ArgumentParser(prog='pixela2img',
                            description='Create image files or objects from pixela graphs.',
                            epilog='Thanks Pixela: https://pixe.la')
    parser.add_argument('-u', '--user-name', required=True, help='Pixela username.')
    parser.add_argument('-g', '--graph', required=True, help='Pixela graph id.')
    parser.add_argument('-m', '--mode', required=False, help='set `short` if you want small graph.')
    parser.add_argument('-d', '--date', required=False,
                        help='set `yyyyMMdd` style date string if you want offset graph.')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_argument()
    date = "{0:%Y%m%d}".format(datetime.now())
    if args.date is not None:
        date = args.date

    converter = Pixela2Img()
    file_name = f"{args.user_name}-{args.graph}-{date}.png"
    converter.convert(args.user_name, args.graph, args.date, args.mode)
    converter.save(file_name)
