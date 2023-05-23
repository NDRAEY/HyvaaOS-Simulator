import pygame

class Widget:
    def __init__(self, window, x, y, width, height):
        self.window = window

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def on_click(self, desktop, event, widget):
        ...

    def on_hover(self, desktop, event, widget):
        ...

    def render(self):
        ...

class Label(Widget):
    def __init__(self, window, text, x, y, color=(0, 0, 0), fontsize=18):
        super().__init__(window, x, y, -1, -1)

        self.text = text
        self.color = color
        self.fontsize = fontsize
        self.font = pygame.font.Font("res/JetBrains.ttf", fontsize)

    def render_text(self):
        rendered =  self.font.render(self.text, True, self.color)

        self.width = rendered.get_width()
        self.height = rendered.get_height()

        return rendered

    def render(self):
        self.window.surface.blit(
            self.render_text(),
            (self.x, self.y)
        )


class Button(Widget):
    def __init__(self, window, label="Button", x=0, y=0, width=None, height=None, color=(255, 255, 255)):
        super().__init__(window, x, y, width, height)

        self.label = Label(self.window, label, 0, 0)

        self.width = self.label.render_text().get_width() + 16
        self.height = self.label.render_text().get_height() + 16

        if width: self.width = width
        if height: self.height = height

        self.color = color

    def render(self):
        textdim = self.label.render_text()
        textdim = textdim.get_width(), textdim.get_height() 

        self.label.x = self.x + (self.width - textdim[0]) // 2
        self.label.y = (self.y + (self.height + textdim[1] - 53) // 2)
        
        pygame.draw.rect(
            self.window.surface,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        self.label.render()

class Group(Widget):
    def __init__(self, window, *widgets) -> None:
        self.widgets: list[Widget] = widgets

        mx = min([i.x for i in self.widgets])
        my = min([i.y for i in self.widgets])
        mw = max([i.width for i in self.widgets])
        mh = max([i.height for i in self.widgets])

        super().__init__(window, mx, my, mw, mh)

    def update(self):
        self.x = min([i.x for i in self.widgets])
        self.y = min([i.y for i in self.widgets])
        self.width = max([i.x + i.width for i in self.widgets])
        self.height = max([i.y + i.height for i in self.widgets])

    def render(self):
        self.update()
        for i in self.widgets:
            i.render()

    def on_click(self, desktop, event, widget):
        for i in self.widgets:
            i.on_click(desktop, event, i)

class VerticalAutoArrangeableGroup(Widget):
    def __init__(self, window, *widgets, padding=3) -> None:
        self.widgets: list[Widget] = list(widgets)
        self.padding = padding

        if not self.widgets:
            super().__init__(window, 0, 0, 0, 0)
            return

        mx = min([i.x for i in self.widgets])
        my = min([i.y for i in self.widgets])
        mw = max([i.width for i in self.widgets])
        mh = max([i.height for i in self.widgets])

        super().__init__(window, mx, my, mw, mh)

    def update(self):
        if not self.widgets:
            return

        for n, i in enumerate(self.widgets[1:]):
            i.y = self.widgets[n].y + self.widgets[n].height + self.padding

        self.x = min([i.x for i in self.widgets])
        self.y = min([i.y for i in self.widgets])
        self.width = max([i.x + i.width for i in self.widgets])
        self.height = max([i.y + i.height for i in self.widgets])

    def render(self):
        self.update()
        for i in self.widgets:
            i.render()

    def on_click(self, desktop, event, widget):
        for i in self.widgets:
            i.on_click(desktop, event, i)

class HorizontalAutoArrangeableGroup(Widget):
    def __init__(self, window, *widgets, padding=3) -> None:
        self.widgets: list[Widget] = widgets
        self.padding = padding

        mx = min([i.x for i in self.widgets])
        my = min([i.y for i in self.widgets])
        mw = max([i.width for i in self.widgets])
        mh = max([i.height for i in self.widgets])

        super().__init__(window, mx, my, mw, mh)

    def update(self):
        for n, i in enumerate(self.widgets[1:]):
            i.x = self.widgets[n].x + self.widgets[n].width + self.padding

        self.x = min([i.x for i in self.widgets])
        self.y = min([i.y for i in self.widgets])
        self.width = max([i.x + i.width for i in self.widgets])
        self.height = max([i.y + i.height for i in self.widgets])

    def render(self):
        self.update()
        for i in self.widgets:
            i.render()

    def on_click(self, desktop, event, widget):
        for i in self.widgets:
            i.on_click(desktop, event, i)

class Image(Widget):
    def __init__(self, window, filename: str, x, y, width = None, height = None):
        super().__init__(window, x, y, width, height)

        self.image = pygame.image.load(filename)
        
        if width:
            self.width = width
        else:
            self.width = self.image.get_height()
        
        if height:
            self.height = height
        else:
            self.height = self.image.get_height()

        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def render(self):
        self.window.surface.blit(
            self.image,
            (self.x, self.y)
        )