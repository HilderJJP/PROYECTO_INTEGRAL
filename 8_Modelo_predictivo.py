import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("compresive_strength_concrete.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo y la variable de entrada
fc = "Concrete compressive strength(MPa, megapascals)"
X = df[["Age (day)"]]
y = df[fc]

# Entrenar el modelo lineal
modelo = LinearRegression()
modelo.fit(X, y)

# Predecir la resistencia para un concreto de 120 días
edad_nueva = pd.DataFrame({"Age (day)": [120]})
resistencia_120 = modelo.predict(edad_nueva)[0]
print(f"Resistencia predicha a los 120 días: {resistencia_120:.2f} MPa")

# Calcular R² sobre los mismos datos usados para entrenar
r2 = modelo.score(X, y)
print(f"R² en los datos de entrenamiento: {r2:.4f}")
