from abc import abstractmethod
from typing import Dict, List
from dataclasses import dataclass
from eazyplotly.constants import APPEARANCE_SETTINGS
from plotly.subplots import make_subplots

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@dataclass
class EzPlotly:
    data: List[List[float | int]] | pd.DataFrame
    fig = None
    title_text_plot = ""
    title_text_xaxis = ""
    title_text_yaxis = ""

    @abstractmethod
    def __create_fig__(self) -> None: ...

    @abstractmethod
    def __format_x_axis__(self, appearance_settings: Dict = APPEARANCE_SETTINGS) -> None:
        self.fig.update_xaxes(
            title_text=self.title_text_xaxis,
            title_font_size=appearance_settings["title_font_size"],
            title_font_family=appearance_settings["title_font_family"],
            ticks=appearance_settings["ticks"],
            color=appearance_settings["color"],
            gridcolor=appearance_settings["gridcolor"],
            griddash=appearance_settings["griddash"],
            linecolor=appearance_settings["linecolor"],
            linewidth=appearance_settings["linewidth"],
            exponentformat=appearance_settings["exponentformat"]
        )

    @abstractmethod
    def __format_y_axis__(self, appearance_settings: Dict = APPEARANCE_SETTINGS) -> None:
        self.fig.update_yaxes(
            title_text=self.title_text_yaxis,
            title_font_size=appearance_settings["title_font_size"],
            title_font_family=appearance_settings["title_font_family"],
            ticks=appearance_settings["ticks"],
            color=appearance_settings["color"],
            gridcolor=appearance_settings["gridcolor"],
            griddash=appearance_settings["griddash"],
            linecolor=appearance_settings["linecolor"],
            linewidth=appearance_settings["linewidth"],
            exponentformat=appearance_settings["exponentformat"]
        )

    @abstractmethod
    def __format_layout__(self, appearance_settings: Dict = APPEARANCE_SETTINGS) -> None:
        self.fig.update_layout(
            title_text=self.title_text_plot,
            showlegend=appearance_settings["showlegend"],
            plot_bgcolor=appearance_settings["plot_bgcolor"],
            paper_bgcolor=appearance_settings["paper_bgcolor"],
            legend=appearance_settings["legend"]
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

    def __create_fig__(self) -> None:
        specs = []
        for n, _ in enumerate(self.secondary):
            spec = [{"secondary_y": self.secondary[n]}]
            specs.append(spec)

        self.fig = make_subplots(
            rows=self.rows,
            cols=self.cols,
            specs=specs
        )

    def __add_trace__(self, scatter_settings: Dict = APPEARANCE_SETTINGS) -> List[go.Scatter]:
        traces = []
        name_idx = 0
        for tn in range(0, self.traces_len, 2):
            trace = go.Scatter(
                x=self.data[tn],
                y=self.data[tn + 1],
                mode=scatter_settings["mode"],
                marker=dict(
                    size=scatter_settings["size"],
                    symbol=scatter_settings["symbol"]
                ),
                name=self.names[name_idx]
            )
            traces.append(trace)
            name_idx += 1
        return traces

    def __scatter_2d__(self, traces):
        self.fig = go.Figure(traces)

    def __format_x_axis__(self) -> None:
        super().__format_x_axis__()

    def __format_y_axis__(self) -> None:
        super().__format_y_axis__()

    def __format_layout__(self) -> None:
        super().__format_layout__()

    def create_plot(self) -> go.Figure:
        self.__create_fig__()
        traces = self.__add_trace__()
        self.__scatter_2d__(traces)

        self.__format_x_axis__()
        self.__format_y_axis__()
        self.__format_layout__()

        return self.fig


class EzScatter3D:
    def __init__(
            self,

    ):
        super().__init__()


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

    def __create_fig__(self) -> None:
        self.fig = px.box(self.data.loc[:, self.variables_to_plot])

    def __format_y_axis__(self) -> None:
        super().__format_y_axis__()

    def __format_x_axis__(self) -> None:
        super().__format_x_axis__()

    def __format_layout__(self) -> None:
        super().__format_layout__()

    def create_plot(self) -> go.Figure:
        self.__create_fig__()
        self.__format_x_axis__()
        self.__format_y_axis__()
        self.__format_layout__()

        return self.fig
