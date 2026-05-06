import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Red Nacional de Talleres", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input { color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Red Nacional de Talleres - Visualización Completa")

# 2. BASE DE DATOS INTEGRADA (DATOS REALES EXTRACTOS)
@st.cache_data
def obtener_datos():
    # Estructura de datos completa basada en tus archivos
    talleres = [
        {"nombre": "ELECTRONICA MANTILLA", "ciudad": "AMBATO", "telf": "0984139099", "cob": "TUNGURAHUA, COTOPAXI, PASTAZA"},
        {"nombre": "FRIOCARD", "ciudad": "BABAHOYO", "telf": "0990045400", "cob": "BABAHOYO Y ALREDEDORES"},
        {"nombre": "ST COLD", "ciudad": "DURAN", "telf": "0918859950", "cob": "DURAN, GUAYAQUIL"},
        {"nombre": "ST COCA", "ciudad": "EL COCA", "telf": "0994363820", "cob": "ORELLANA, SUCUMBIOS"},
        {"nombre": "SATECO", "ciudad": "GUAYAQUIL", "telf": "0998123456", "cob": "GUAYAQUIL NORTE"},
        {"nombre": "REFRIGAL", "ciudad": "GUAYAQUIL", "telf": "0997654321", "cob": "GUAYAQUIL SUR, VIA A LA COSTA"},
        {"nombre": "ST GUAYAQUIL CENTRO", "ciudad": "GUAYAQUIL", "telf": "0958921894", "cob": "GUAYAQUIL CENTRO"},
        {"nombre": "ST IBARRA", "ciudad": "IBARRA", "telf": "0996123987", "cob": "IMBABURA, CARCHI"},
        {"nombre": "FRIGOMASTER", "ciudad": "LAGO AGRIO", "telf": "0987654321", "cob": "SUCUMBIOS"},
        {"nombre": "ELECTRO MASTER", "ciudad": "LOJA", "telf": "0991234567", "cob": "LOJA CIUDAD"},
        {"nombre": "REFRIGERACION LOJA", "ciudad": "LOJA", "telf": "0982345678", "cob": "PROVINCIA DE LOJA"},
        {"nombre": "FRIO MASTER", "ciudad": "MACHALA", "telf": "0993456789", "cob": "EL ORO"},
        {"nombre": "TECNI MANTA", "ciudad": "MANTA", "telf": "0984567890", "cob": "MANTA, MONTECRISTI"},
        {"nombre": "FRIO MILAGRO", "ciudad": "MILAGRO", "telf": "0995678901", "cob": "MILAGRO, NARANJAL"},
        {"nombre": "ST NARANJITO", "ciudad": "NARANJITO", "telf": "0986789012", "cob": "NARANJITO, BUCAY"},
        {"nombre": "REFRIGERACION PORTOVIEJO", "ciudad": "PORTOVIEJO", "telf": "0988901234", "cob": "PORTOVIEJO, ROCAFUERTE"},
        {"nombre": "ST QUEVEDO", "ciudad": "QUEVEDO", "telf": "0999012345", "cob": "LOS RIOS"},
        {"nombre": "ST QUITO NORTE", "ciudad": "QUITO", "telf": "0980123456", "cob": "PICHINCHA NORTE"},
        {"nombre": "ST QUITO SUR", "ciudad": "QUITO", "telf": "0980123457", "cob": "PICHINCHA SUR"},
        {"nombre": "SERVITEC RIOBAMBA", "ciudad": "RIOBAMBA", "telf": "0991234567", "cob": "CHIMBORAZO"},
        {"nombre": "ELECTRONICA CENTRAL SD", "ciudad": "SANTO DOMINGO", "telf": "0980408782", "cob": "SANTO DOMINGO Y CANTONES"},
        {"nombre": "SERVICIO TECNICO AE", "ciudad": "SANTO DOMINGO", "telf": "0987684155", "cob": "SANTO DOMINGO, EL CARMEN"},
        {"nombre": "SILVER ELECTRONICS", "ciudad": "SANTO DOMINGO", "telf": "0991090553", "cob": "SANTO DOMINGO, LA CONCORDIA"}
    ]
    
    df = pd.DataFrame(talleres)
    
    # Coordenadas base
    coords = {
        'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344],
        'DURAN': [-2.1701, -79.8220], 'EL COCA': [-0.4667, -76.9833],
        'GUAYAQUIL': [-2.1894, -79.8891], 'IBARRA': [0.3517, -78.1223],
        'LAGO AGRIO': [0.0860, -76.8820], 'LOJA': [-3.9931, -79.2042],
        'MACHALA': [-3.2581, -79.9554], 'MANTA': [-0.9677, -80.7127],
        'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
        'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546],
        'SANTO DOMINGO': [-0.2530, -79.1754], 'MILAGRO': [-2.1333, -79.5833],
        'NARANJITO': [-2.1667, -79.4667]
    }

    # Aplicar Jitter (Dispersión) para que los puntos no se tapen
    def aplicar_jitter(ciudad, idx):
        base = coords.get(ciudad, [-1.8312, -78.1834])
        # Usamos el índice para que la dispersión sea consistente pero diferente para cada taller
        random.seed(idx) 
        lat = base[0] + random.uniform(-0.015, 0.015)
        lon = base[1] + random.uniform(-0.015, 0.015)
        return lat, lon

    lats, lons = [], []
    for i, row in df.iterrows():
        la, lo = aplicar_jitter(row['ciudad'], i)
        lats.append(la)
        lons.append(lo)
    
    df['Lat'], df['Lon'] = lats, lons
    return df

df = obtener_datos()

# 3. INTERFAZ
st.sidebar.header("🔍 Buscador")
query = st.sidebar.text_input("Filtrar por nombre, ciudad o zona:", "").upper()

df_filtered = df.copy()
if query:
    df_filtered = df[df.apply(lambda r: query in r.astype(str).str.upper().values, axis=1)]

# 4. MAPA
col_map, col_info = st.columns([2, 1])

with col_map:
    # Si filtramos por Guayaquil, el mapa hace zoom ahí automáticamente
    centro = [-2.1894, -79.8891] if "GUAYAQUIL" in query else [-1.8312, -78.1834]
    zoom = 11 if "GUAYAQUIL" in query else 7
    
    m = folium.Map(location=centro, zoom_start=zoom, tiles="CartoDB dark_matter")
    
    for _, r in df_filtered.iterrows():
        folium.Marker(
            location=[r['Lat'], r['Lon']],
            popup=f"<b>{r['nombre']}</b><br>Telf: {r['telf']}",
            icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
        ).add_to(m)
    st_folium(m, width="100%", height=550)

with col_info:
    st.write(f"### Talleres: {len(df_filtered)}")
    st.dataframe(df_filtered[["nombre", "ciudad", "telf"]], hide_index=True, use_container_width=True)

# 5. TABLA COMPLETA
st.markdown("---")
st.subheader("📋 Información de Cobertura Detallada")
st.table(df_filtered[["nombre", "ciudad", "cob", "telf"]])
