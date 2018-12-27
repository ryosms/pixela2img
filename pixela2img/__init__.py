"""
pixela2img
~~~~~~~~~~

Convert to image files or objects from Pixela graphs.

:copyright: (c) 2018 ryosms, All rights reserved.
:license: MIT
"""
from logging import getLogger, StreamHandler, DEBUG
from xml.etree.ElementTree import Element

import requests
from PIL import Image, ImageDraw
from defusedxml import ElementTree


def pixela2img_logger(name, *, level=DEBUG):
    logger = getLogger(name)
    handler = StreamHandler()
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


class Pixela2Img:
    PIXEL_SIZE = 10
    PIXEL_MARGIN = 2

    def __init__(self, *, logger=None):
        self.image = None
        self.logger = logger or pixela2img_logger(__name__)

    def convert(self, user, graph, date=None, mode=None) -> Image:
        svg = self._svg_from_text(self._load_graph(user, graph, date, mode))
        graph_root = svg[1]
        pixels = []
        for line in graph_root:
            pixels.append(self._parse_line(line))

        self._create_image([p for p in pixels if len(p) > 0])
        return self.image

    def save(self, path: str):
        if self.image is None:
            raise RuntimeError
        self.logger.debug(f"image path: {path}")
        self.image.save(path)

    def _load_graph(self, user, graph, date, mode):
        endpoint = f"https://pixe.la/v1/users/{user}/graphs/{graph}"
        params = {}
        if mode is not None:
            params['mode'] = mode
        if date is not None:
            params['date'] = date
        self.logger.debug(f"{endpoint}: {params}")
        response = requests.get(endpoint, params)
        self.logger.debug(f"response: {response.status_code}")
        if response.status_code != 200:
            self.logger.error(response.content)
            raise RuntimeError
        return response.content

    def _create_image(self, pixels):
        width = (self.PIXEL_SIZE + self.PIXEL_MARGIN) * len(pixels) - self.PIXEL_MARGIN
        height = (self.PIXEL_SIZE + self.PIXEL_MARGIN) * 7 - self.PIXEL_MARGIN
        self.image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        self.logger.debug(f"image size: {self.image.size}")

        x = 0
        for pixels_for_week in pixels:
            y = 0
            for pixel in pixels_for_week:
                d = ImageDraw.Draw(self.image)
                d.rectangle((x, y, x + self.PIXEL_SIZE, y + self.PIXEL_SIZE), pixel)
                y += (self.PIXEL_SIZE + self.PIXEL_MARGIN)
            x += (self.PIXEL_SIZE + self.PIXEL_MARGIN)

    def _parse_line(self, elements):
        pixels = []
        for elem in elements:
            attr = elem.attrib
            if 'data-date' not in attr:
                break
            pixels.append(self._rgb_from_html_color(attr['fill']))

        return pixels

    @staticmethod
    def _svg_from_text(svg_text: str) -> Element:
        return ElementTree.fromstring(svg_text)

    @staticmethod
    def _rgb_from_html_color(html_color: str) -> tuple:
        # expected -> #FFFFFF
        return (int(html_color[1:3], 16),
                int(html_color[3:5], 16),
                int(html_color[5:7], 16))
