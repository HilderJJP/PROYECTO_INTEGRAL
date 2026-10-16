import pandas as pd
import plotly.express as px

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("compresive_strength_concrete.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir las variables del dataset
fc = "Concrete compressive strength(MPa, megapascals)"
cemento = "Cement (component 1)(kg in a m^3 mixture)"
escoria = "Blast Furnace Slag (component 2)(kg in a m^3 mixture)"
ceniza = "Fly Ash (component 3)(kg in a m^3 mixture)"
agua = "Water  (component 4)(kg in a m^3 mixture)"
superplastificante = "Superplasticizer (component 5)(kg in a m^3 mixture)"
agregado_grueso = "Coarse Aggregate  (component 6)(kg in a m^3 mixture)"
agregado_fino = "Fine Aggregate (component 7)(kg in a m^3 mixture)"

# Cada punto representa una mezcla medida a una edad determinada.
fig = px.scatter_3d(
    df,
    x="Age (day)",
    y=cemento,
    z=fc,
    color=agua,
    color_continuous_scale="Viridis",
    opacity=0.8,
    hover_data={
        escoria: ":.1f",
        ceniza: ":.1f",
        superplastificante: ":.1f",
        agregado_grueso: ":.1f",
        agregado_fino: ":.1f",
    },
    title="Edad, diseño de mezcla y resistencia del concreto",
    labels={
        "Age (day)": "Edad del concreto (días)",
        cemento: "Cemento (kg/m³)",
        fc: "Resistencia a la compresión (MPa)",
        agua: "Agua (kg/m³)",
        escoria: "Escoria de alto horno (kg/m³)",
        ceniza: "Ceniza volante (kg/m³)",
        superplastificante: "Superplastificante (kg/m³)",
        agregado_grueso: "Agregado grueso (kg/m³)",
        agregado_fino: "Agregado fino (kg/m³)",
    },
)

fig.update_traces(marker={"size": 4})
fig.update_layout(
    scene={
        "xaxis_title": "Edad (días)",
        "yaxis_title": "Cemento (kg/m³)",
        "zaxis_title": "Resistencia (MPa)",
        "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.2}},
    },
    coloraxis_colorbar={"title": "Agua (kg/m³)"},
)

fig.show()


