import widget

class Calculator:
    def __init__(self, winsys):
        self.winsys = winsys
        self.window = winsys.new_window("Calculator", 45, 45, 225, 300)
        
        self.val = ""
        self.widget_names = "789C456+123-0/*="

        self.result_label = widget.Label(self.window, self.val, 25, 15, (255, 255, 255))

        self.window.widgets.append(
            self.result_label
        )

        for i in range(0, 4):
            for j in range(0, 4):
                btn = widget.Button(self.window, self.widget_names[i * 4 + j], 25 + (j * 50), 50 + (i * 50))
                btn.on_click = self.process_key

                self.window.widgets.append(btn)

    def process_key(self, desktop, event, widget: widget.Button):
        if widget.label.text == "=":
            if len(self.val) == 0:
                return
        
            try:
                self.val = str(eval(self.val))
            except:
                self.val = "Error"
            
            self.result_label.text = self.val
            return
        elif widget.label.text == "C":
            self.val = ""
            self.result_label.text = self.val
            
            return

        self.val += widget.label.text
        self.result_label.text = self.val
