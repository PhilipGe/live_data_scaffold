from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.label import Label

from graphboard.graph_model import GraphModel
from graphboard.plot_model import PlotModel
from kivy.uix.gridlayout import GridLayout

class GraphBoard(BoxLayout):
    
    def __init__(self, graph_models: list[GraphModel], **kwargs):
        super(GraphBoard, self).__init__(**kwargs)

        self.orientation = 'vertical'
        # self.padding = (10,100,10,10)

        self.graphs = []

        for graph in graph_models:
            self.add_widget(Label(text=graph.title, height=50, size_hint_y=None))

            self.graphs.append(Graph(
                xlabel = graph.x_label,
                ylabel = graph.y_label,
                xmin = graph.x_bounds[0],
                xmax = graph.x_bounds[1],
                ymin = graph.y_bounds[0],
                ymax = graph.y_bounds[1],
                padding = 2
            ))

            self.add_widget(self.graphs[-1])

            for plot in graph.plots:
                m = MeshLinePlot(color=plot.color)
                plot.attach_meshlineplot(m)
                self.graphs[-1].add_plot(m)