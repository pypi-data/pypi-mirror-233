from abc import abstractmethod, ABC
from typing import List
from constants import AppearanceSettings as aps
from plotly.subplots import make_subplots

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class EzPlotly(ABC):
    def __init__(
            self,
            data: List[List[float | int]] | pd.DataFrame,
            fig=None,
            title_text_plot="",
            title_text_xaxis="",
            title_text_yaxis=""
    ):
        self.data = data
        self.fig = fig
        self.title_text_plot = title_text_plot
        self.title_text_xaxis = title_text_xaxis
        self.title_text_yaxis = title_text_yaxis

    @abstractmethod
    def _create_fig_(self) -> None: ...

    def _format_x_axis_(self) -> None:
        self.fig.update_xaxes(
            title_text=self.title_text_xaxis,
            title_font_size=aps.title_font_size,
            title_font_family=aps.title_font_family,
            ticks=aps.ticks,
            color=aps.color,
            gridcolor=aps.gridcolor,
            griddash=aps.griddash,
            linecolor=aps.linecolor,
            linewidth=aps.linewidth,
            exponentformat=aps.exponentformat
        )

    def _format_y_axis_(self) -> None:
        self.fig.update_yaxes(
            title_text=self.title_text_yaxis,
            title_font_size=aps.title_font_size,
            title_font_family=aps.title_font_family,
            ticks=aps.ticks,
            color=aps.color,
            gridcolor=aps.gridcolor,
            griddash=aps.griddash,
            linecolor=aps.linecolor,
            linewidth=aps.linewidth,
            exponentformat=aps.exponentformat
        )

    def _format_layout_(self) -> None:
        self.fig.update_layout(
            title_text=self.title_text_plot,
            showlegend=aps.showlegend,
            plot_bgcolor=aps.plot_bgcolor,
            paper_bgcolor=aps.paper_bgcolor,
            legend=aps.legend
        )


class EzScatter2D(EzPlotly):
    """
    For traces --> [x1, y1, x2, y2,...,xn, yn]; where xn and yn are list of floats or ints
    """

    def __init__(
            self,
            data: List[List[float | int]] | pd.DataFrame,
            rows: int, cols: int,
            secondary: List[bool], names: List[str],
            title_text_plot: str = "Plot",
            title_text_xaxis: str = "X",
            title_text_yaxis: str = "Y"
    ) -> None:
        super().__init__(data)
        self.data = data
        self.rows = rows
        self.cols = cols
        self.names = names
        self.secondary = secondary
        self.title_text_plot = title_text_plot
        self.title_text_xaxis = title_text_xaxis
        self.title_text_yaxis = title_text_yaxis
        self.fig = None

    @property
    def traces_len(self):
        return len(self.data)

    def _create_fig_(self) -> None:
        specs = []
        for n, _ in enumerate(self.secondary):
            spec = [{"secondary_y": self.secondary[n]}]
            specs.append(spec)

        self.fig = make_subplots(
            rows=self.rows,
            cols=self.cols,
            specs=specs
        )

    def __add_trace__(self) -> List[go.Scatter]:
        traces = []
        name_idx = 0
        for tn in range(0, self.traces_len, 2):
            trace = go.Scatter(
                x=self.data[tn],
                y=self.data[tn + 1],
                mode=aps.mode,
                marker=dict(
                    size=aps.size,
                    symbol=aps.symbol
                ),
                name=self.names[name_idx]
            )
            traces.append(trace)
            name_idx += 1
        return traces

    def __scatter_2d__(self, traces):
        self.fig = go.Figure(traces)

    def create_plot(self) -> go.Figure:
        self._create_fig_()
        traces = self.__add_trace__()
        self.__scatter_2d__(traces)

        self._format_x_axis_()
        self._format_y_axis_()
        self._format_layout_()

        return self.fig


class EzBox(EzPlotly):
    def __init__(
            self,
            data: pd.DataFrame,
            variables_to_plot: List[str],
            title_text_plot: str = "Plot",
            title_text_xaxis: str = "",
            title_text_yaxis: str = ""
    ):
        super().__init__(data)
        self.data = data
        self.variables_to_plot = variables_to_plot
        self.title_text_plot = title_text_plot
        self.title_text_xaxis = title_text_xaxis
        self.title_text_yaxis = title_text_yaxis
        self.fig = None

    def _create_fig_(self) -> None:
        self.fig = px.box(self.data.loc[:, self.variables_to_plot])

    def create_plot(self) -> go.Figure:
        self._create_fig_()
        self._format_x_axis_()
        self._format_y_axis_()
        self._format_layout_()

        return self.fig


# To be continued...
# class EzScatter3D:
#     def __init__(
#             self,
#
#     ):
#         super().__init__()
