from matplotlib.patches import Rectangle

from gui.canvases.base_canvas import BaseCanvas
import numpy as np


class BaseBarCanvas(BaseCanvas):

    def __init__(self, figure_title='', x_axis_title='', y_axis_title=''):
        super().__init__(figure_title, x_axis_title, y_axis_title)
        self._initialize_figure()

    def _add_hover(self):
        self.figure.canvas.mpl_connect('pick_event', self._handle_pick)
        self.annotation = self.axes.annotate("", xy=(0, 0), xytext=(0.5, 30), textcoords="offset points",
                                             bbox=dict(boxstyle="round", fc="yellow", ec="b", lw=2),
                                             arrowprops=dict(arrowstyle="->"))
        self.annotation.set_visible(False)

    def _handle_pick(self, event):
        if isinstance(event.artist, Rectangle):
            self._handle_rectangle_pick(event)
        else:
            print("Unknown event")

    def _handle_rectangle_pick(self, event):
        rectangle = event.artist
        mouse_event = event.mouseevent

        label = self._get_rectangle_label(rectangle)

        self.annotation.set_visible(True)
        height = rectangle.get_height()
        x = mouse_event.xdata
        y = mouse_event.ydata
        self.annotation.xy = (x, y)
        if label is None:
            text = f"{height:0.0f}"
        else:
            text = f"{label}: {height:0.0f}"
        self.annotation.set_text(text)
        self.annotation.get_bbox_patch().set_alpha(0.4)
        self.figure.canvas.draw_idle()

    def _get_rectangle_label(self, rectangle):
        handles, labels = rectangle.axes.get_legend_handles_labels()
        labels = [label for h, label in zip(handles, labels) if rectangle in h.get_children()]
        if len(labels) == 1:
            label = labels[0]
        else:
            label = None
        return label

    def _plot_bar(self, y, x_labels=None, x_offset=0.0, plot_average=True, color="b", add_hover=True, *args, **kwargs):
        x = np.array([k for k in range(len(y))])
        if x_labels is None:
            x_labels = ['' for k in y]

        n = int(x.shape[0] / 15)
        if n == 0:
            n = 1
        x_subset = x[::n]
        x_labels_subset = x_labels[::n]

        self.axes.bar(x + x_offset, y, color=color, picker=add_hover, *args, **kwargs)

        if plot_average:
            y_mean = [np.mean(y) for _ in y]
            self.axes.plot(x, y_mean, "--", color=color)

        self.axes.set_xticks(x_subset)
        self.axes.set_xticklabels(x_labels_subset, rotation=-60)

        if add_hover:
            self._add_hover()
