import pandas as pd
import plotly.express as px

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("compresive_strength_concrete.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Calcular correlaciones entre las columnas numéricas
corr = df.corr(numeric_only=True)

# Crear el mapa de calor
fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Mapa de correlaciones",
    labels={"color": "Correlación"},
)

fig.show()

