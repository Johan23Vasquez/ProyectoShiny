from shiny import App, ui, reactive
from shinywidgets import output_widget, render_plotly
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from shared import simpsons_park, COLORES, ESCALA_CALIFICACION, FECHA_MIN, FECHA_MAX, TEMPORADAS
from components.paneles import panel_rating, panel_cap_a_cap, panel_all_cap
from components.server import server

app_ui = ui.page_navbar(
    panel_rating(),
    panel_cap_a_cap(),
    panel_all_cap,
    title="Los Simpsons vs South Park",
)

app_ui = ui.page_navbar(
    panel_rating(),
    panel_cap_a_cap(),
    panel_all_cap(),
    title="Los Simpsons vs South Park",
)
    
app = App(app_ui, server)
