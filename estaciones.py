from numpy.lib.shape_base import column_stack
from pandas.core.tools.datetimes import to_datetime
import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

import plotly.io as pio





try:
	db = mysql.connector.connect(
				host = "www.dev.factoriaccp.cl",
				user = st.secrets["db_username"],
				password = st.secrets["db_password"],
				database = "factoria_estaciones",
            	connection_timeout=15
				)
except:
	print("Hubo problemas al conectarse en la DB")

query = "SELECT fecha,orp_1,orp_2,conductividad, tds FROM estacion_v52_1 ORDER BY id DESC"
cursor = db.cursor(buffered=True)
cursor.execute(query)
data = cursor.fetchall()

st.header("Estaciones de monitoreo remoto")

pio.templates.default = "seaborn"
st.header("")
fig_2 = go.Figure()
st.sidebar.header("Selector de estaciones")
estacion = st.sidebar.selectbox(
	"Elija una estación",
	("Estación 1","Estación 2","Estación 3")
)
st.sidebar.select_slider("Seleccione cuántos datos desea ver",options=[30,40,50,60])
st.sidebar.button("Descargar los datos de: " + estacion)
columns = ["Fecha","Conductividad","TDS","ORP","ORP 2"]
df = pd.DataFrame(data,columns=columns)
df = df.iloc[-10:]

for column in columns[1:]:
	fig_2.add_trace(go.Scatter(x=df["Fecha"], y=df[column].astype(float),
					mode="lines+markers",
					name=column))
	fig_2.update_layout(hovermode='x unified',
						title=estacion)

st.write(fig_2)


st.header("Ubicación de " + estacion)
st.write("")
map = pd.DataFrame(
	np.random.randn(10, 2) / [50, 50] + [37.76, -122.4],
	columns=['lat', 'lon'])

st.map(map)

st.write("")
st.subheader("Datos")
st.write("")
st.dataframe(df)


cursor.close()
db.close()