from shiny import reactive
from shinywidgets import render_plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from shared import (
    simpsons_park,
    COLORES,
    ESCALA_CALIFICACION,
)

def server(input, output, session):

    @reactive.calc
    def filtrar_datos():
        fechas = input.fechas()

        f1 = pd.to_datetime(fechas[0])
        f2 = pd.to_datetime(fechas[1])

        return simpsons_park[
            (simpsons_park["serie"].isin(input.series_t1()))
            & (simpsons_park["fecha_estreno"] >= f1)
            & (simpsons_park["fecha_estreno"] <= f2)
        ]

    @reactive.calc
    def filtrar_temporada():
        return simpsons_park[
            simpsons_park["temporada"] == int(input.temporadas())
        ]

    @reactive.calc
    def filtrar_datos_pestania3():
        return simpsons_park[
            simpsons_park["serie"].isin(input.series_t3())
        ]

    @output
    @render_plotly
    def grafica_rating():
        data = filtrar_datos()

        if data.empty:
            return go.Figure()

        fig = go.Figure()

        for serie in input.series_t1():
            sub = data[data["serie"] == serie]

            if sub.empty:
                continue

            fig.add_trace(
                go.Scatter(
                    x=sub["fecha_estreno"],
                    y=sub["rating"],
                    mode="lines",
                    name=serie,
                    line=dict(color=COLORES.get(serie, "gray")),
                )
            )

        fig.update_layout(
            title="Ratings de episodios a lo largo del tiempo",
            xaxis_title="Fecha de estreno",
            yaxis_title="Rating",
            height=500,
        )

        return fig

    @output
    @render_plotly
    def grafica_calor_comparativa():
        data = filtrar_temporada()

        escala_calificacion = [
            [0.0, "rgb(215, 48, 39)"],
            [0.5, "rgb(254, 224, 144)"],
            [1.0, "rgb(26, 152, 80)"],
        ]

        fig = go.Figure(
            data=go.Heatmap(
                x=data["episodio"],
                y=data["serie"],
                z=data["rating"],
                colorscale=escala_calificacion,
                zmin=5,
                zmax=10,
                xgap=2,
                ygap=5,
                colorbar=dict(title="Rating IMDb"),
                hovertemplate="<b>%{y}</b><br>Episodio: %{x}<br>Rating: %{z}<extra></extra>",
            )
        )

        fig.update_layout(
            title=f"Comparativa de Ratings por Temporada {input.temporadas()}",
            xaxis_title="Número de Episodio",
            yaxis_title="Serie",
            height=300,
        )

        return fig

    @output
    @render_plotly
    def grafica_calor():
        data = filtrar_datos_pestania3()

        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Los Simpsons", "South Park"),
            shared_yaxes=False,
        )

        sub_simpsons = data[data["serie"] == "Los Simpsons"]

        if not sub_simpsons.empty:
            fig.add_trace(
                go.Heatmap(
                    x=sub_simpsons["temporada"],
                    y=sub_simpsons["episodio"],
                    z=sub_simpsons["rating"],
                    colorscale=ESCALA_CALIFICACION,
                    zmin=5,
                    zmax=10,
                    colorbar=dict(title="Rating", x=0.45),
                    hovertemplate="Temporada: %{x}<br>Episodio: %{y}<br>Rating: %{z}<extra></extra>",
                ),
                row=1,
                col=1,
            )

        sub_spark = data[data["serie"] == "South Park"]

        if not sub_spark.empty:
            fig.add_trace(
                go.Heatmap(
                    x=sub_spark["temporada"],
                    y=sub_spark["episodio"],
                    z=sub_spark["rating"],
                    colorscale=ESCALA_CALIFICACION,
                    zmin=5,
                    zmax=10,
                    colorbar=dict(title="Rating", x=1.0),
                    hovertemplate="Temporada: %{x}<br>Episodio: %{y}<br>Rating: %{z}<extra></extra>",
                ),
                row=1,
                col=2,
            )

        fig.update_layout(
            title="Calificaciones de Episodios: Temporada vs Número de Episodio",
            height=600,
        )

        fig.update_yaxes(
            title_text="Número de Episodio",
            autorange="reversed",
            row=1,
            col=1,
        )

        fig.update_yaxes(
            title_text="Número de Episodio",
            autorange="reversed",
            row=1,
            col=2,
        )

        fig.update_xaxes(
            title_text="Temporada",
            row=1,
            col=1,
        )

        fig.update_xaxes(
            title_text="Temporada",
            row=1,
            col=2,
        )

        return fig