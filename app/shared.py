from pathlib import Path
import pandas as pd

data_dir = (Path(__file__).parent / "../data/processed").resolve()

simpsons = pd.read_parquet(data_dir / "simpsons.parquet")
south_park = pd.read_parquet(data_dir / "south_park.parquet")

simpsons["serie"] = "Los Simpsons"
south_park["serie"] = "South Park"

simpsons_park = pd.concat(
    [simpsons, south_park],
    ignore_index=True
)

COLORES = {
    "Los Simpsons": "orange",
    "South Park": "blue"
}

ESCALA_CALIFICACION = [
    [0.0, "rgb(215, 48, 39)"],
    [0.5, "rgb(254, 224, 144)"],
    [1.0, "rgb(26, 152, 80)"]
]

FECHA_MIN = simpsons_park["fecha_estreno"].min()
FECHA_MAX = simpsons_park["fecha_estreno"].max()

TEMPORADAS = [
    str(i)
    for i in sorted(simpsons_park["temporada"].unique())
]