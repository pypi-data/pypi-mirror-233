""""""

from celestine.typed import (
    N,
    R,
)
from celestine.window import Window as Window_
from celestine.window.collection import Rectangle
from celestine.window.element import Abstract as Abstract_
from celestine.window.element import Button as Button_
from celestine.window.element import Image as Image_
from celestine.window.element import Label as Label_


class Abstract(Abstract_):
    """"""


class Button(Abstract, Button_):
    """"""

    def callback(self, *_):
        """
        The object callback.

        callback(self, sender, app_data, user_data)
        """
        self.call(self.action, **self.argument)

    def make(self, ring, **star):
        """"""
        dearpygui = ring.package.dearpygui

        dearpygui.add_button(
            callback=self.callback,
            label=self.data,
            tag=self.name,
            pos=self.area.origin,
        )


class Image(Abstract, Image_):
    """
    Manages image objects.

    delete_item(...)
    """

    def make(self, ring, **star):
        """
        Draw the image to screen.

        image = (0, 0, 0, [])
        width = image[0]
        height = image[1]
        channels = image[2]
        photo = image[3]
        """

        dearpygui = ring.package.dearpygui

        path = str(self.path)
        image = dearpygui.load_image(path)
        width = image[0]
        height = image[1]
        # channels = image[2]
        photo = image[3]

        with dearpygui.texture_registry(show=False):
            dearpygui.add_dynamic_texture(
                default_value=photo,
                height=height,
                tag=self.name,
                width=width,
            )

        dearpygui.add_image(
            self.name,
            tag=f"{self.name}-base",
            pos=self.area.origin,
        )

    def update(self, ring: R, image, **star):
        """"""
        dearpygui = ring.package.dearpygui
        super().update(ring, image, **star)

        path = str(self.path)
        image = dearpygui.load_image(path)
        # width = image[0]
        # height = image[1]
        # channels = image[2]
        photo = image[3]

        dearpygui.set_value(self.name, photo)


class Label(Abstract, Label_):
    """"""

    def make(self, ring, **star):
        """"""

        dearpygui = ring.package.dearpygui

        dearpygui.add_text(
            f" {self.data}",  # extra space hack to fix margin error
            tag=self.name,
            pos=self.area.origin,
        )


class Window(Window_):
    """"""

    def extension(self):
        """"""
        return [
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".gif",
            ".hdr",
            ".pic",
            ".pbm",
            ".pgm",
            ".ppm",
            ".pnm",
        ]

    def make(self, ring, **star):
        dearpygui = ring.package.dearpygui
        for name, item in self.item.items():
            with item.canvas:
                dearpygui.configure_item(item.name, show=False)
                item.make(ring)

    def setup(self, name):
        """"""
        dearpygui = self.ring.package.dearpygui
        canvas = dearpygui.window(tag=name)
        return canvas

    def turn(self, page, **star):
        """"""
        dearpygui = self.ring.package.dearpygui

        dearpygui.hide_item(self.page.name)

        super().turn(page, **star)

        tag = self.page.name
        dearpygui.show_item(tag)
        dearpygui.set_primary_window(tag, True)

    def __enter__(self):
        super().__enter__()

        dearpygui = self.ring.package.dearpygui

        title = self.ring.language.APPLICATION_TITLE
        dearpygui.create_context()
        width, height = self.area.origin
        dearpygui.create_viewport(
            title=title,
            small_icon="celestine_small.ico",
            large_icon="celestine_large.ico",
            width=width,
            height=height,
            x_pos=256,
            y_pos=256,
            min_width=640,
            max_width=3840,
            min_height=480,
            max_height=2160,
            resizable=True,
            vsync=True,
            always_on_top=False,
            decorated=True,
            clear_color=(0, 0, 0),
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        dearpygui = self.ring.package.dearpygui

        dearpygui.setup_dearpygui()
        dearpygui.show_viewport(minimized=False, maximized=False)
        dearpygui.start_dearpygui()
        dearpygui.destroy_context()
        return False

    def __init__(self, ring: R, **star) -> N:
        element = {
            "button": Button,
            "image": Image,
            "label": Label,
        }
        area = Rectangle(0, 0, 960, 640)
        canvas = None
        super().__init__(ring, canvas, element, area, **star)
        self.tag = "window"
