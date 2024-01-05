from typing import Tuple, Callable
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot

class PointStream: 

    def __init__(self, stream: Callable[[],list[Tuple[int,int]]], poll_interval_s: int, cumulative, max_num_points, color):
        self.stream: Callable[[],list[Tuple[int,int]]] = stream
        self.cumulative: bool = cumulative
        self.max_num_points: int = max_num_points
        self.poll_interval_s = poll_interval_s
        self.curr_data = []
        self.color = color

        self.meshlineplot = None

        self.minx = 0
        self.maxx = 100
        self.miny = 0
        self.maxy = 100

    def attach_meshlineplot(self, meshlineplot: MeshLinePlot):
        self.meshlineplot = meshlineplot

    def new_data(self, data: list[Tuple[int,int]]):
        relevant = data[-self.max_num_points:]
        if(self.cumulative):
            self.curr_data.extend(data)
            self.curr_data = self.curr_data[-self.max_num_points:]
        else:
            self.curr_data = relevant

        self.update_mins_and_maxes()

        if(self.meshlineplot != None): 
            self.meshlineplot.points = self.curr_data

    def initiate_stream(self):
        self.new_data(self.stream())
        Clock.schedule_once(lambda dt: self.initiate_stream(), self.poll_interval_s)

    def update_mins_and_maxes(self):
        self.minx, self.miny = self.curr_data[0]
        self.maxx, self.maxy = self.curr_data[0]

        for x,y in self.curr_data:
            if(x < self.minx): self.minx = x
            elif(x > self.maxx): self.maxx = x

            if(y < self.miny): self.miny = y
            elif(y > self.maxy): self.maxy = y