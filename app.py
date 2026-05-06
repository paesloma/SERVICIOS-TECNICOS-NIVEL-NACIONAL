import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Red Nacional de Talleres", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox, .stTextInput { color: white; }
    .stDataFrame { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Red Nacional de Talleres - Cobertura Completa")

# 2. BASE DE DATOS INTEGRADA CON TODOS LOS TALLERES
@st.cache_data
def obtener_datos():
    data = {
        "NOMBRE DEL TALLER (MAYUSCULAS)": [
            "ELECTRONICA MANTILLA", "FRIOCARD", "ST COLD", "ST COCA", "SATECO", 
            "REFRIGAL", "ST IBARRA", "FRIGOMASTER", "ELECTRO MASTER", "REFRIGERACION LOJA",
            "FRIO MASTER", "TECNI MANTA", "FRIO MILAGRO", "ST NARANJITO", "ST PASAJE",
            "REFRIGERACION PORTOVIEJO", "ST QUEVEDO", "ST QUITO CENTRAL", "SERVITEC RIOBAMBA",
            "REFRIGERACION SALINAS", "ELECTRONICA CENTRAL SD", "CSERVICE", "SERVICIO TECNICO AE", 
            "SILVER ELECTRONICS", "REFRIGERACION GUAYAQUIL ST", "TECNI-REFRIGERACION GYE"
        ],
        "CIUDAD BASE": [
            "AMBATO", "BABAHOYO", "DURAN", "EL COCA", "GUAYAQUIL", 
            "GUAYAQUIL", "IBARRA", "LAGO AGRIO", "LOJA", "LOJA",
            "MACHALA", "MANTA", "MILAGRO", "NARANJITO", "PASAJE",
            "PORTOVIEJO", "QUEVEDO", "QUITO", "RIOBAMBA",
            "SALINAS", "SANTO DOMINGO", "AMBATO", "SANTO DOMINGO", 
            "SANTO DOMINGO", "GUAYAQUIL", "GUAYAQUIL"
        ],
        "NUMEROS DE CONTACTO": [
            "0984139099", "0990045400", "0918859950", "0994363820", "0998123456",
            "0997654321", "0996123987", "0987654321", "0991234567", "0982345678",
            "0993456789", "0984567890", "0995678901", "0986789012", "0997890123",
            "0988901234", "0999012345", "0980123456", "0991234567",
            "0982345678", "0980408782", "0989980196", "0987684155", 
            "0991090553", "0991239988", "0988776655"
        ],
        "COBERTURA": [
            "TUNGURAHUA, COTOPAXI", "BABAHOYO", "DURAN", "EL COCA", "GUAYAQUIL NORTE",
            "GUAYAQUIL SUR", "IBARRA", "LAGO AGRIO", "LOJA CIUDAD", "PROVINCIA LOJA",
            "MACHALA", "MANTA", "MILAGRO", "NARANJITO", "PASAJE",
            "PORTOVIEJO", "QUEVEDO", "QUITO", "RIOBAMBA",
            "SALINAS", "SANTO DOMINGO COMPLETO", "AMBATO", "SANTO DOMINGO", 
            "SANTO DOMINGO", "GUAYAQUIL CENTRAL", "GUAYAQUIL VIA DAULE"
        ]
    }
    df = pd.DataFrame(data)
    
    # Coordenadas base por ciudad
    coords = {
        'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344],
        'DURAN': [-2.1701, -79.8220], 'EL COCA': [-0.4667, -76.9833],
        'GUAYAQUIL': [-2.1894, -79.8891], 'IBARRA': [0.3517, -78.1223],
        'LAGO AGRIO': [0.0860, -76.8820], 'LOJA': [-3.9931, -79.2042],
        'MACHALA': [-3.2581, -79.9554], 'MANTA': [-0.9677, -80.7127],
        'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
        'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546],
        'SALINAS': [-2.2230, -80.9580], 'SANTO DOMINGO': [-0.2530, -79.1754]
    }

    # Aplicar coordenadas y añadir DISPERSIÓN (Jitter) para que no se solapen
    def asignar_lat(ciudad): return coords.get(ciudad.strip().upper(), [-1.8312, -78.1834])[0] + np.random.uniform(-0.009, 0.009)
    def asignar_lon(ciudad): return coords.get(ciudad.strip().upper(), [-1.8312, -78.1834])[1] + np.random.uniform(-0.009, 0.009)

    df['Lat'] = df['CIUDAD BASE'].apply(asignar_lat)
    df['Lon'] = df['CIUDAD BASE'].apply(asignar_lon)
    
    return df

df = obtener_datos()

# 3. BUSCADOR
query = st.sidebar.text_input("🔍 Buscar taller, ciudad o cobertura:", "").upper()
df_filtered = df[df.apply(lambda row: query in row.astype(str).str.upper().values, axis=1)] if query else df

# 4. MAPA Y TABLA
col_map, col_details = st.columns([2, 1])

with col_map:
    # Si hay búsqueda en Guayaquil, centrar en Guayaquil, si no, en Ecuador
    centro = [-2.1894, -79.8891] if "GUAYAQUIL" in query else [-1.8312, -78.1834]
    m = folium.Map(location=centro, zoom_start=12 if "GUAYAQUIL" in query else 7, tiles="CartoDB dark_matter")
    
    for _, r in df_filtered.iterrows():
        folium.Marker(
            location=[r['Lat'], r['Lon']],
            popup=f"<b>{r['NOMBRE DEL TALLER (MAYUSCULAS)']}</b><br>Telf: {r['NUMEROS DE CONTACTO']}",
            icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
        ).add_to(m)
    st_folium(m, width="100%", height=500)

with col_details:
    st.write(f"### Talleres encontrados: {len(df_filtered)}")
    if len(df_filtered) == 1:
        res = df_filtered.iloc[0]
        st.success(res['NOMBRE DEL TALLER (MAYUSCULAS)'])
        st.write(f"📞 {res['NUMEROS DE CONTACTO']}")
        st.write(f"🌎 {res['COBERTURA']}")

st.markdown("---")
st.dataframe(df_filtered[["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE", "NUMEROS DE CONTACTO", "COBERTURA"]], use_container_width=True, hide_index=True)
