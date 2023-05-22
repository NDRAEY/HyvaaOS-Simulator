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
        return self.font.render(self.text, True, self.color)

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