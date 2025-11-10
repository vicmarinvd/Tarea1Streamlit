import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carga de datos
def load_data():
    df = pd.read_excel('/Users/victoriamarin/Downloads/vendedores.xlsx')
    return df

data = load_data()

st.title("Ventas Dashboard")

# Filtro por Región
region_filter = st.multiselect(
    "Selecciona una o varias regiones:",
    options=data['REGION'].unique(),
    default=data['REGION'].unique()
)

filtered_data = data[data['REGION'].isin(region_filter)] #busca las regiones seleccionadas en el multiselect

st.subheader("Datos filtrados por Región")
st.dataframe(filtered_data)

# Grafica de Unidades Vendidas
st.subheader("Unidades Vendidas por Región")
units = filtered_data.groupby('REGION')['UNIDADES VENDIDAS'].sum()

fig1, ax1 = plt.subplots()
ax1.bar(units.index, units.values, color='purple')
ax1.set_xlabel("Región")
ax1.set_ylabel("Unidades Vendidas")
ax1.set_title("Unidades Vendidas por Región")
st.pyplot(fig1)

# Gráfica de Ventas Totales 
st.subheader("Gráfica de Ventas Totales por Región")
sales_total = filtered_data.groupby('REGION')['VENTAS TOTALES'].sum().reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x='REGION', y='VENTAS TOTALES', data=sales_total, color='purple')  
plt.title('Ventas Totales por Región')
st.pyplot(plt)

# Gráfica de Porcentaje de Ventas
st.subheader("Porcentaje de Ventas por Región")
sales_total = filtered_data.groupby('REGION')['VENTAS TOTALES'].sum().reset_index()
total_sales = sales_total['VENTAS TOTALES'].sum()
percentages = (sales_total['VENTAS TOTALES'] / total_sales) * 100

fig3, ax3 = plt.subplots()
ax3.pie(percentages, labels=sales_total['REGION'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
ax3.set_title("Porcentaje de Ventas por Región")
st.pyplot(fig3)

# Datos de un vendedor específico 
st.subheader("Datos de un Vendedor Específico")

vendedor_selected = st.selectbox(
    "Selecciona un Vendedor:",
    options=filtered_data['APELLIDO'].unique()
)

vendedor_data = filtered_data[filtered_data['APELLIDO'] == vendedor_selected]

st.write(vendedor_data)

# Resumen del vendedor
st.write(f"**Total de Unidades Vendidas por {vendedor_selected}:** {vendedor_data['UNIDADES VENDIDAS'].sum()}")
st.write(f"**Total de Ventas por {vendedor_selected}:** {vendedor_data['VENTAS TOTALES'].sum()}")
st.write(f"**Porcentaje de Ventas de {vendedor_selected}:** {vendedor_data['PORCENTAJE DE VENTAS'].iloc[0]:.2f}%")
