from typing import Tuple, Callable
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot

class PlotModel: 

    def __init__(self, stream: Callable[[],list[Tuple[int,int]]], poll_interval_s: int, cumulative, max_num_points, color):
        self.stream: Callable[[],list[Tuple[int,int]]] = stream
        self.cumulative: bool = cumulative
        self.max_num_points: int = max_num_points
        self.poll_interval_s = poll_interval_s
        self.curr_data = []
        self.color = color

        self.meshlineplot = None

    def attach_meshlineplot(self, meshlineplot: MeshLinePlot):
        self.meshlineplot = meshlineplot

    def new_data(self, data: list[Tuple[int,int]]):
        relevant = data[-self.max_num_points:]
        if(self.cumulative):
            self.curr_data.extend(data)
            self.curr_data = self.curr_data[-self.max_num_points:]
        else:
            self.curr_data = relevant

        if(self.meshlineplot != None): 
            self.meshlineplot.points = self.curr_data

    def initiate_stream(self):
        self.new_data(self.stream())
        Clock.schedule_once(lambda dt: self.initiate_stream(), self.poll_interval_s)