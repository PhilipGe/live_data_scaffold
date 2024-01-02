from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class GraphBoard(BoxLayout):
    
    def __init__(self, **kwargs):
        super(GraphBoard, self).__init__(**kwargs)

        self.add_widget(Button())