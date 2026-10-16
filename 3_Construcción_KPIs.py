import pandas as pd

# Cargar el dataset y eliminar filas duplicadas
df = pd.read_csv("compresive_strength_concrete.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo
fc = "Concrete compressive strength(MPa, megapascals)"

# Calcular KPIs
resistencia_promedio = df[fc].mean()
resistencia_maxima = df[fc].max()
resistencia_minima = df[fc].min()
cantidad_registros = df.shape[0]
edad_promedio = df["Age (day)"].mean()

# Mostrar resultados
print(f"Resistencia promedio: {resistencia_promedio:.2f} MPa")
print(f"Resistencia máxima: {resistencia_maxima:.2f} MPa")
print(f"Resistencia mínima: {resistencia_minima:.2f} MPa")
print(f"Número de registros: {cantidad_registros}")
print(f"Edad promedio: {edad_promedio:.2f} días")
