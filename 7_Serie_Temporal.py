import pandas as pd
import plotly.express as px

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("compresive_strength_concrete.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo
fc = "Concrete compressive strength(MPa, megapascals)"
componentes = [
    "Cement (component 1)(kg in a m^3 mixture)",
    "Blast Furnace Slag (component 2)(kg in a m^3 mixture)",
    "Fly Ash (component 3)(kg in a m^3 mixture)",
    "Water  (component 4)(kg in a m^3 mixture)",
    "Superplasticizer (component 5)(kg in a m^3 mixture)",
    "Coarse Aggregate  (component 6)(kg in a m^3 mixture)",
    "Fine Aggregate (component 7)(kg in a m^3 mixture)",
]

# Calcular promedios de resistencia y componentes de mezcla para cada edad
serie = df.groupby("Age (day)")[[fc, *componentes]].mean().reset_index()

etiquetas = {
    "Age (day)": "Edad del concreto (días)",
    fc: "Resistencia promedio (MPa)",
    componentes[0]: "Cemento (kg/m³)",
    componentes[1]: "Escoria de alto horno (kg/m³)",
    componentes[2]: "Ceniza volante (kg/m³)",
    componentes[3]: "Agua (kg/m³)",
    componentes[4]: "Superplastificante (kg/m³)",
    componentes[5]: "Agregado grueso (kg/m³)",
    componentes[6]: "Agregado fino (kg/m³)",
}

# Visualizar la evolución de la resistencia según la edad
fig = px.line(
    serie,
    x="Age (day)",
    y=fc,
    markers=True,
    hover_data={componente: ":.1f" for componente in componentes},
    title="Resistencia promedio y diseño de mezcla por edad",
    labels=etiquetas,
)

fig.show()