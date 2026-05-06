import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Red Nacional de 41 Talleres", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input { color: white; }
    .stDataFrame { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Red Nacional de Talleres con Direcciones Exactas")

# 2. BASE DE DATOS INTEGRAL CON DIRECCIONES
@st.cache_data
def obtener_datos_expertos():
    data = {
        "NOMBRE DEL TALLER": [
            'ELECTRONICA MANTILLA ', 'FRIOCARD', 'ST COLD', 'MULTISERVICIOS JACK', 'SERVIAIRE ECUADOR', 'PROVATEC', 'CLiMA FRIO', 'JR ELECTRIC', 'MULTITECH RUDY  CEDENO', 'CLISERIN', 'DIGICASLE CENTRO DIGITAL SA', 'PROSERVICIO SAS', 'CISTRONIC ', 'BOR AIR', 'REFRICLIMAMORAN', 'ELECTRÓNICA S.A', 'GAMASERVICES', 'FRIO-STAR', 'RRSERVICENTERRYC', 'KLIMASMART', 'SERVITEC - RONNY BARREZUETA ', 'TALLER DEL SALTO ', 'SERVICIO TECNICO PURO FRIO', 'CLIMAFRIO NARANJITO', 'SERVICIO TÉCNICO CASA FRIA', 'SERMATEC PORTOVIEJO', 'ELECTRONICA 3D', 'TECNIRIOS-ASC', 'Servifrio ', 'Tecnicservice ', 'MEGASERVICE', 'SERMATEC ELECTRONICA', 'MASTERTECH', 'GAMA ELECTRONICS', 'CSTE ELECTRONICA', 'SERVICECOOL ', 'SERVIELEC', 'SERVICIO TECNICO AE', 'SILVER ELECTRONICS', 'ELECTRONICA CENTRAL', 'CSERVICE'
        ],
        "CIUDAD": [
            'AMBATO', 'BABAHOYO', 'DURAN', 'EL COCA', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'IBARRA', 'LAGO AGRIO', 'LAGO AGRIO', 'LOJA', 'MACHALA', 'MANTA', 'MANTA', 'MILAGRO', 'NARANJITO', 'PASAJE', 'PORTOVIEJO', 'PORTOVIEJO', 'QUEVEDO', 'QUEVEDO', 'QUEVEDO', 'QUITO', 'QUITO', 'QUITO', 'RIOBAMBA', 'RIOBAMBA', 'SALINAS', 'SANTO DOMINGO', 'SANTO DOMINGO', 'SANTO DOMINGO', 'SANTO DOMINGO', 'AMBATO'
        ],
        "DIRECCION": [
            'QUIS QUIS Y ATAHUALPA', 'EL SALTO', 'CDLA CARLOS CARRERA MZA S11', 'BARRIO EL MORETAL', 'CDLA BELLAVISTA', 'CDLA. LOS ALMENDROS', 'COOP. 5 DE DICIEMBRE', 'VIA DAULE KM 8.5', 'GUASMO CENTRAL', 'MAPASINGUE OESTE', 'AV. DE LAS AMERICAS', 'CDLA. ADACE', 'URB. PORTÓN DEL RÍO', 'BASTION POPULAR', 'VILLA ESPAÑA 2', 'AV. MARIANO ACOSTA', 'BARRIO CENTRAL', 'AV. QUITO', 'AV. SALVADOR BUSTAMANTE', 'AV. 25 DE JUNIO', 'AV. 4 DE NOVIEMBRE', 'CALLE 119 AV 108', 'CDLA. LAS PIÑAS', 'CALLE GUAYAQUIL', 'AV. ROCAFUERTE', 'CALLE ALAJUELA', 'AV. METROPOLITANA', 'AV. REVOLUCION CIUDADANA', 'CALLE 7 DE OCTUBRE', 'AV. WALTER ANDRADE', 'AV. DE LA PRENSA', 'AV. MALDONADO', 'AV. REAL AUDIENCIA', 'AV. DANIEL LEON BORJA', 'CALLE 10 DE AGOSTO', 'AV. PRINCIPAL SALINAS', 'AV. ABRAHAM CALAZACON', 'COOP. NUEVA REPUBLICA', 'CALLE PEDRO VICENTE MALDONADO', 'CALLE IERRA COLORADA', 'ISIDRO VITERI Y TRES CARABELAS'
        ],
        "CONTACTO": [
            '0984139099', '0990045400', '0989842610', '0939407412', '0990965410', '0992821856', '0967899084', '0959628723', '0967588262', '0963091210', '0980684211', '0967550764', '0997898383', '0995583678', '0968139739', '0994234714', '0992897319', '0997620929', '0987533656', '0993647218', '0982808932', '0994406002', '0990510831', '0999637012', '0967432580', '0993549420', '0968485502', '0999221879', '0997949393', '0989078967', '0978928040', '0985706276', '0998260143', '0994215004', '0982868384', '0992048071', '0982553943', '0987684155', '0991090553', '0980408782', '0989980196'
        ]
    }
    df = pd.DataFrame(data)
    
    # Coordenadas base
    coords = {
        'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344], 'DURAN': [-2.1701, -79.8220],
        'EL COCA': [-0.4667, -76.9833], 'GUAYAQUIL': [-2.1894, -79.8891], 'IBARRA': [0.3517, -78.1223],
        'LAGO AGRIO': [0.0860, -76.8820], 'LOJA': [-3.9931, -79.2042], 'MACHALA': [-3.2581, -79.9554],
        'MANTA': [-0.9677, -80.7127], 'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
        'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546], 'SALINAS': [-2.2230, -80.9580],
        'SANTO DOMINGO': [-0.2530, -79.1754], 'NARANJITO': [-2.1667, -79.4667], 'PASAJE': [-3.3250, -79.8070],
        'MILAGRO': [-2.1333, -79.5833]
    }

    # Dispersión circular para que se vean todos en la misma ciudad
    def get_lat(c, i): return coords.get(c, [-1.8312, -78.1834])[0] + (np.sin(i)*0.015)
    def get_lon(c, i): return coords.get(c, [-1.8312, -78.1834])[1] + (np.cos(i)*0.015)

    df['Lat'] = [get_lat(c, i) for i, c in enumerate(df['CIUDAD'])]
    df['Lon'] = [get_lon(c, i) for i, c in enumerate(df['CIUDAD'])]
    return df

df = obtener_datos_expertos()

# 3. INTERFAZ
st.sidebar.header("🔍 Filtro de Red")
busqueda = st.sidebar.text_input("Buscar por taller, ciudad o calle:", "").upper()

df_filtered = df.copy()
if busqueda:
    mask = df.apply(lambda r: busqueda in r.astype(str).str.upper().values, axis=1)
    df_filtered = df[mask]

# 4. VISUALIZACIÓN
col_map, col_list = st.columns([2, 1])

with col_map:
    # Ajuste de vista
    centro = [-1.8312, -78.1834]
    zoom = 7
    if "GUAYAQUIL" in busqueda: centro, zoom = [-2.1894, -79.8891], 12
    
    m = folium.Map(location=centro, zoom_start=zoom, tiles="CartoDB dark_matter")
    for _, r in df_filtered.iterrows():
        folium.Marker(
            location=[r['Lat'], r['Lon']],
            popup=folium.Popup(f"<b>{r['NOMBRE DEL TALLER']}</b><br>📍 {r['DIRECCION']}<br>📞 {r['CONTACTO']}", max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    st_folium(m, width="100%", height=500)

with col_list:
    st.metric("Total de Talleres", len(df_filtered))
    st.write("### Direcciones Rápidas")
    st.dataframe(df_filtered[["NOMBRE DEL TALLER", "DIRECCION"]], hide_index=True)

# 5. TABLA COMPLETA
st.markdown("---")
st.subheader("📋 Detalle Completo de Ubicaciones")
st.table(df_filtered[["NOMBRE DEL TALLER", "CIUDAD", "DIRECCION", "CONTACTO"]])
