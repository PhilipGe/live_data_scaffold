from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.graph import MeshLinePlot, Graph
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from graphboard.graph.graph_model import GraphModel
from graphboard.graph.stream import PointStream 
from graphboard.graph.graph_tile import GraphTile

class GraphBoard(BoxLayout):
    
    def __init__(self, graph_models: list[GraphModel], **kwargs):
        super(GraphBoard, self).__init__(**kwargs)

        self.orientation = 'vertical'
        # self.padding = (10,100,10,10)

        self.graphs = []

        for graph_model in graph_models:
            self.add_widget(Label(text=graph_model.title, height=50, size_hint_y=None))

            tile = GraphTile(graph_model)

            self.graphs.append(tile.graph)

            self.add_widget(tile)

            for stream in graph_model.streams:
                m = MeshLinePlot(color=stream.color)
                stream.attach_meshlineplot(m)
                tile.graph.add_plot(m)