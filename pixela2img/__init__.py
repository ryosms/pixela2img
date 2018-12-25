from xml.etree.ElementTree import Element

import requests
from PIL import Image, ImageDraw
from defusedxml import ElementTree


class Pixela2Img:
    PIXEL_SIZE = 10
    PIXEL_MARGIN = 2

    def __init__(self):
        self.image = None

    def convert(self, user, graph, date=None, mode=None) -> Image:
        svg = self._svg_from_text(self._load_graph(user, graph, date, mode))
        graph_root = svg[1]
        start_pos = 0
        pixels = []
        for line in graph_root:
            pixels.extend(self._parse_line(line, start_pos))
            start_pos += self.PIXEL_SIZE + self.PIXEL_MARGIN
        self._create_image(pixels)
        return self.image

    def save(self, path: str):
        if self.image is None:
            raise RuntimeError
        self.image.save(path)

    @staticmethod
    def _load_graph(user, graph, date, mode):
        endpoint = f"https://pixe.la/v1/users/{user}/graphs/{graph}"
        params = {}
        if mode is not None:
            params['mode'] = mode
        if date is not None:
            params['date'] = date
        response = requests.get(endpoint, params)
        if response.status_code != 200:
            raise RuntimeError
        return response.content

    def _create_image(self, pixels):
        width = pixels[-1]['x'] + self.PIXEL_SIZE
        height = pixels[6]['y'] + self.PIXEL_SIZE
        self.image = Image.new('RGBA', (width, height), (255, 255, 255, 0))

        for pixel in pixels:
            x = pixel['x']
            y = pixel['y']
            d = ImageDraw.Draw(self.image)
            d.rectangle((x, y, x + self.PIXEL_SIZE, y + self.PIXEL_SIZE), pixel['fill'])

    def _parse_line(self, elements, start_x: int):
        pixels = []
        height = 0
        for elem in elements:
            attr = elem.attrib
            if 'data-date' not in attr:
                break
            fill = self._rgb_from_html_color(attr['fill'])
            pixels.append({'x': start_x, 'y': height, 'fill': fill})
            height += self.PIXEL_SIZE + self.PIXEL_MARGIN

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
