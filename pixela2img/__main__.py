from argparse import ArgumentParser
from datetime import datetime
from logging import INFO, DEBUG

from pixela2img import Pixela2Img, pixela2img_logger


def _parse_argument():
    parser = ArgumentParser(prog='pixela2img',
                            description='Create a `png` image file from a pixela graph.',
                            epilog='Thanks Pixela: https://pixe.la')
    parser.add_argument('-u', '--user-name', required=True, help='Pixela username.')
    parser.add_argument('-g', '--graph', required=True, help='Pixela graph id.')
    parser.add_argument('-m', '--mode', required=False, help='set `short` if you want small graph.')
    parser.add_argument('-d', '--date', required=False,
                        help='set `yyyyMMdd` style date string if you want offset graph.')
    parser.add_argument('--debug', required=False, help='show debug log.',
                        action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_argument()
    level = DEBUG if args.debug else INFO
    logger = pixela2img_logger(f"pixela2img cli({__name__}", level=level)
    logger.debug(args)
    date = "{0:%Y%m%d}".format(datetime.now())
    if args.date is not None:
        date = args.date

    converter = Pixela2Img(logger=logger)
    file_name = f"{args.user_name}-{args.graph}-{date}.png"
    converter.convert(args.user_name, args.graph, args.date, args.mode)
    converter.save(file_name)
    logger.info('finish!')
