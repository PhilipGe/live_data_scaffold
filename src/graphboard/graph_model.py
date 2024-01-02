from graphboard.plot_model import PlotModel

class GraphModel:

    def __init__(self, title, x_label, y_label, x_bounds=[0,100], y_bounds=[0,1]):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.plots: list[PlotModel] = []

    def add_plot(self, plot: PlotModel):
        self.plots.append(plot)

    def initiate_plot_streams(self):
        for plot in self.plots: plot.initiate_stream()