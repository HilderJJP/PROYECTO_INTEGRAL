from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression


st.set_page_config(
    page_title="Dashboard de resistencia del concreto",
    page_icon="🏗️",
    layout="wide",
)

DATASET = Path(_file_).resolve().parent / "compresive_strength_concrete.csv"
FC = "Concrete compressive strength(MPa, megapascals)"
EDAD = "Age (day)"
COMPONENTES = {
    "Cemento": "Cement (component 1)(kg in a m^3 mixture)",
    "Escoria de alto horno": "Blast Furnace Slag (component 2)(kg in a m^3 mixture)",
    "Ceniza volante": "Fly Ash (component 3)(kg in a m^3 mixture)",
    "Agua": "Water  (component 4)(kg in a m^3 mixture)",
    "Superplastificante": "Superplasticizer (component 5)(kg in a m^3 mixture)",
    "Agregado grueso": "Coarse Aggregate  (component 6)(kg in a m^3 mixture)",
    "Agregado fino": "Fine Aggregate (component 7)(kg in a m^3 mixture)",
}

st.title("Dashboard de resistencia del concreto")
st.caption("Indicadores, análisis de mezclas y predicción de resistencia")

if not DATASET.is_file():
    st.error(f"No se encontró el archivo del dataset: {DATASET}")
    st.stop()

df = pd.read_csv(DATASET)
df.columns = df.columns.str.strip()

columnas_requeridas = [FC, EDAD, *COMPONENTES.values()]
faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]
if faltantes:
    st.error("Faltan columnas requeridas en el CSV: " + ", ".join(faltantes))
    st.stop()

filas_originales = len(df)
df = df.drop_duplicates().copy()
duplicados_eliminados = filas_originales - len(df)

with st.sidebar:
    st.header("Datos")
    st.write(f"Registros cargados: *{filas_originales:,}*")
    st.write(f"Duplicados completos excluidos: *{duplicados_eliminados:,}*")
    st.write(f"Registros analizados: *{len(df):,}*")
    st.caption("Los análisis excluyen filas idénticas en todas sus columnas.")

media = df[FC].mean()
mediana = df[FC].median()
moda = df[FC].mode().iloc[0]
desviacion_estandar = df[FC].std()

tab_resumen, tab_distribucion, tab_mezclas, tab_correlaciones, tab_modelo = st.tabs(
    ["Resumen", "Distribución", "Mezclas y edad", "Correlaciones", "Modelo predictivo"]
)

with tab_resumen:
    st.subheader("Indicadores clave (KPIs)")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Resistencia promedio", f"{media:.2f} MPa")
    kpi2.metric("Resistencia máxima", f"{df[FC].max():.2f} MPa")
    kpi3.metric("Resistencia mínima", f"{df[FC].min():.2f} MPa")
    kpi4.metric("Registros analizados", f"{len(df):,}")
    kpi5.metric("Edad promedio", f"{df[EDAD].mean():.2f} días")

    st.subheader("Vista previa del dataset limpio")
    st.dataframe(df.head(10), use_container_width=True)

with tab_distribucion:
    st.subheader("Distribución de la resistencia")
    st.caption(
        f"Media: {media:.2f} MPa · Mediana: {mediana:.2f} MPa · "
        f"Moda: {moda:.2f} MPa · Desviación estándar: {desviacion_estandar:.2f} MPa"
    )
    histograma = px.histogram(
        df,
        x=FC,
        nbins=30,
        title="Distribución de la resistencia del concreto",
        labels={FC: "Resistencia a la compresión (MPa)", "count": "Frecuencia"},
    )
    for valor, nombre, color, estilo in [
        (media, "Media", "red", "dash"),
        (moda, "Moda", "green", "dot"),
        (mediana, "Mediana", "blue", "dashdot"),
    ]:
        histograma.add_vline(
            x=valor,
            line_dash=estilo,
            line_color=color,
            annotation_text=f"{nombre}: {valor:.2f}",
        )
    st.plotly_chart(histograma, use_container_width=True)

with tab_mezclas:
    st.subheader("Edad, diseño de mezcla y resistencia")
    st.markdown(
        "Cada punto representa una mezcla. Gira el gráfico y coloca el cursor sobre un "
        "punto para consultar las cantidades de sus componentes."
    )
    ingredientes = list(COMPONENTES.values())
    nombres_componentes = list(COMPONENTES.keys())
    scatter3d = px.scatter_3d(
        df,
        x=EDAD,
        y=COMPONENTES["Cemento"],
        z=FC,
        color=FC,
        color_continuous_scale="Viridis",
        opacity=0.8,
        hover_data={
            columna: ":.1f"
            for columna in ingredientes
            if columna != COMPONENTES["Cemento"]
        },
        title="Edad y cantidad de cemento frente a la resistencia",
        labels={
            EDAD: "Edad del concreto (días)",
            COMPONENTES["Cemento"]: "Cemento (kg/m³)",
            FC: "Resistencia a la compresión (MPa)",
            **{
                columna: f"{nombre} (kg/m³)"
                for nombre, columna in COMPONENTES.items()
            },
        },
    )
    scatter3d.update_traces(marker={"size": 4})
    scatter3d.update_layout(
        scene={
            "xaxis_title": "Edad (días)",
            "yaxis_title": "Cemento (kg/m³)",
            "zaxis_title": "Resistencia (MPa)",
            "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.2}},
        },
        coloraxis_colorbar={"title": "Resistencia (MPa)"},
    )
    st.plotly_chart(scatter3d, use_container_width=True)

    serie = df.groupby(EDAD)[[FC, *ingredientes]].mean().reset_index()
    etiquetas = {
        EDAD: "Edad del concreto (días)",
        FC: "Resistencia promedio (MPa)",
        **{
            columna: f"{nombre} (kg/m³)"
            for nombre, columna in COMPONENTES.items()
        },
    }
    lineas = px.line(
        serie,
        x=EDAD,
        y=FC,
        markers=True,
        hover_data={columna: ":.1f" for columna in ingredientes},
        title="Resistencia promedio y diseño de mezcla por edad",
        labels=etiquetas,
    )
    st.plotly_chart(lineas, use_container_width=True)
    st.caption(
        "En la serie por edad, los componentes muestran el promedio de las mezclas "
        "observadas a esa edad; el gráfico 3D muestra los valores de cada registro."
    )

with tab_correlaciones:
    st.subheader("Mapa de calor de correlaciones")
    correlaciones = df.corr(numeric_only=True)
    mapa = px.imshow(
        correlaciones,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Correlación entre variables numéricas",
        labels={"color": "Correlación"},
    )
    st.plotly_chart(mapa, use_container_width=True)
    st.caption("La correlación describe asociación lineal; no implica causalidad.")

with tab_modelo:
    st.subheader("Predicción con regresión lineal")
    st.write("El modelo usa únicamente la edad del concreto para predecir su resistencia.")
    edad_prediccion = st.number_input(
        "Edad para la predicción (días)",
        min_value=0,
        max_value=3650,
        value=120,
        step=1,
    )

    X = df[[EDAD]]
    y = df[FC]
    modelo = LinearRegression()
    modelo.fit(X, y)
    entrada = pd.DataFrame({EDAD: [edad_prediccion]})
    resistencia_predicha = modelo.predict(entrada)[0]
    r2 = modelo.score(X, y)

    resultado1, resultado2 = st.columns(2)
    resultado1.metric(
        f"Resistencia predicha a los {edad_prediccion} días",
        f"{resistencia_predicha:.2f} MPa",
    )
    resultado2.metric("R² en datos de entrenamiento", f"{r2:.4f}")
    st.warning(
        "Este modelo usa solo la edad y su R² se calcula con los mismos datos usados "
        "para entrenarlo. La predicción no considera la composición de la mezcla y "
        "puede ser poco precisa."
    )