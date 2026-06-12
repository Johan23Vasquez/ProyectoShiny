from shiny import App, ui, reactive 
from shinywidgets import output_widget, render_widget, render_plotly
import plotly.graph_objects as go 
import pandas as pd 
from plotly.subplots import make_subplots 
import sys
from pathlib import Path

from shared import FECHA_MAX, FECHA_MIN, TEMPORADAS

ruta_raiz = Path(__file__).resolve().parent.parent
if str(ruta_raiz) not in sys.path:
    sys.path.append(str(ruta_raiz))

#from shared import simpsons_park, COLORES, ESCALA_CALIFICACION, FECHA_MIN, FECHA_MAX, TEMPORADAS


def panel_rating():
    return ui.nav_panel( 
        "Rating a traves del tiempo", 
        ui.layout_sidebar( 
            ui.sidebar( 
                ui.input_checkbox_group( 
                    "series_t1", 
                    "series", 
                    choices=["Los Simpsons", "South Park"], 
                    selected=["Los Simpsons", "South Park"] 
                ), 
                ui.input_date_range( 
                    "fechas", 
                    "Rango de fechas", 
                    start=str(FECHA_MIN.date()), 
                    end=str(FECHA_MAX.date()) 
                ) 
            ), 
            ui.card( 
                ui.card_header("Comparativa de Ratings Los Simpsons vs South Park"), 
                output_widget("grafica_rating"), 
            ) 
        ) 
    )

def panel_cap_a_cap():
    return ui.nav_panel(
        "Vs de capitulo a capitulo",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select(
                    "temporadas",
                    "Temporada",
                    choices=TEMPORADAS,
                    selected="1"
                )
            ),
            ui.card(
                ui.card_header("Distribución de Ratings por Temporada y Episodio"),
                output_widget("grafica_calor_comparativa"),
            )
        )
    )

def panel_all_cap():
    return ui.nav_panel(
        "Calificacion de todos los capitulos",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_checkbox_group(
                    "series_t3", "series",
                    choices=["Los Simpsons", "South Park"],
                    selected=["Los Simpsons", "South Park"]
                ),
            ),
            ui.card(
                ui.card_header("Calificación de cada capitulo de cada Programa"),
                output_widget("grafica_calor"),
            )
        )
    )

