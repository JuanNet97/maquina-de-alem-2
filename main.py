import streamlit as st
from openai import OpenAI
import json

# --- 1. CONFIGURACIÓN VISUAL (ESTÉTICA COMPLETA) ---
st.set_page_config(page_title="La Máquina de Alem", page_icon="🇦🇷", layout="centered")

st.markdown("""
    <style>
    /* 1. FONDO Y ESTRUCTURA (Forzamos !important para anular modo oscuro) */
    .stApp { 
        background-color: #f4f4f4 !important; 
        border-top: 20px solid #D32F2F !important; 
    }
    
    /* 2. TIPOGRAFÍA */
    h1 { 
        color: #D32F2F !important; 
        font-family: 'Helvetica', sans-serif; 
        font-weight: 900; 
        text-transform: uppercase; 
        letter-spacing: -1px; 
        margin-bottom: 5px; 
    }
    
    /* Subtítulos y textos generales */
    h3, p, .stMarkdown { 
        font-family: 'Georgia', serif; 
        color: #333333 !important;
    }
    
    /* CAJA 1: LA FRASE RADICAL (Impacto) */
    .headline-box {
        background-color: #D32F2F !important;
        color: white !important;
        padding: 30px;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 1.8rem;
        text-transform: uppercase;
        border-radius: 5px;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(211, 47, 47, 0.3);
        line-height: 1.1;
        border: 2px solid #B71C1C !important;
    }

    /* CAJA 2: TESIS (Análisis) */
    .thesis-box {
        background-color: #fff !important;
        padding: 25px;
        border-left: 10px solid #212121 !important;
        font-family: 'Georgia', serif;
        color: #333 !important;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .thesis-label {
        font-size: 0.8rem;
        font-weight: 800;
        color: #9E9E9E !important;
        text-transform: uppercase;
        display: block;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .meme-name {
        color: #D32F2F !important;
        font-weight: 900;
        font-size: 1.4rem;
        text-transform: uppercase;
        display: block;
        margin-bottom: 10px;
    }
    
    /* CAJA 3: EVIDENCIA (Cita) */
    .quote-box {
        background-color: #ECEFF1 !important;
        padding: 20px;
        font-style: italic;
        border-right: 8px solid #B71C1C !important;
        color: #37474F !important;
        margin-bottom: 25px;
        font-size: 1rem;
        border-radius: 5px;
    }
    .quote-author {
        text-align: right;
        font-weight: bold;
        color: #B71C1C !important;
        font-size: 0.9rem;
        margin-top: 10px;
        text-transform: uppercase;
        font-family: 'Helvetica', sans-serif;
    }

   /* BOTONES (Corrección de contraste) */
    .stButton > button { 
        background-color: #212121 !important; /* Fondo Negro */
        color: #FFFFFF !important; /* TEXTO BLANCO PURO OBLIGATORIO */
        border: 2px solid #212121 !important; 
        font-weight: 900 !important; 
        width: 100%; 
        padding: 15px; 
        font-size: 1.1rem;
        text-transform: uppercase; 
        transition: 0.3s; 
        border-radius: 5px;
    }
    
    /* Arreglo específico: A veces Streamlit usa etiquetas <p> dentro del botón */
    .stButton > button p {
        color: #FFFFFF !important; 
    }

    /* Estado Hover (Al pasar el mouse/dedo) */
    .stButton > button:hover { 
        background-color: #424242 !important; 
        color: #FFFFFF !important;
        border-color: #424242 !important;
        transform: translateY(-2px); 
    }
    
    /* Estado Focus/Active (Al hacer click) */
    .stButton > button:focus, .stButton > button:active {
        color: #FFFFFF !important;
        background-color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN CON OPENAI ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ CRÍTICO: No se detectó la API Key. Configurala en 'Secrets'.")
    st.stop()

# --- 3. CARGA DE CONOCIMIENTO (SIN LÍMITES) ---
@st.cache_data
def cargar_conocimiento():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read() 
    except FileNotFoundError:
        st.error("⚠️ Error: Falta el archivo 'conocimiento.txt'. Cárgalo en GitHub.")
        st.stop()

base_de_conocimiento = cargar_conocimiento()

# --- 4. INTERFAZ DE USUARIO ---

st.title("/// LA MÁQUINA DE ALEM")
st.markdown("### ¿Qué dice el radicalismo sobre...")

st.info("""
**PROYECTO ACADÉMICO EXPERIMENTAL** Desarrollado en el marco de la investigación de Juan Ignacio Net como parte de su trabajo final de la **Maestría en Comunicación Política de la Universidad Austral**.

Esta API está alimentada exclusivamente por los resultados de la investigación sobre los discursos de los máximos referentes históricos de la Unión Cívica Radical.

⚙️ *El modelo se encuentra actualmente en fase de calibración.*
""")
tema_usuario = st.text_input("", placeholder="Ej: El veto a las universidades, los jubilados, la corrupción...")

col1, col2 = st.columns([0.65, 0.35])
with col1:
    boton = st.button("HACER HABLAR AL RADICALISMO")
with col2:
    generar_img = st.checkbox("Generar Meme", value=True)

# --- 5. LÓGICA DE PROCESAMIENTO ---
# --- 6. LÓGICA DE PROCESAMIENTO ---
if boton:
    if tema_usuario:
        with st.spinner("Analizando doctrina histórica..."):
            
            # --- PROMPT CORREGIDO: LÍNEA DESARROLLADA + CONEXIÓN TEÓRICA ---
            prompt_sistema = f"""
            Eres el sistema experto "La Máquina de Alem". Tu cerebro es EXCLUSIVAMENTE esta Tesis de Maestría y el Archivo Histórico de la UCR.
            
            TEXTO FUENTE:
            {base_de_conocimiento}

            TU MISIÓN:
            El usuario plantea el tema: "{tema_usuario}".

            INSTRUCCIONES DE GENERACIÓN (ESTRICTAS):
            1. **FRASE RADICAL (Recuadro Rojo):** NO escribas un slogan corto de marketing. Escribe una **sentencia política desarrollada y contundente** (1 o 2 oraciones completas) que fije la postura del partido sobre el tema. Debe tener peso retórico y profundidad ideológica.
            2. **EL SIGNIFICANTE (Tesis):** Identifica qué concepto de la tesis (ej: La Reparación, La Ética, El Régimen) se activa con este tema.
            3. **EXPLICACIÓN (Justificación):** Explica técnicamente **por qué** la frase que escribiste arriba se relaciona con ese Significante de la Tesis. (Ej: "Esta frase invoca la 'Reparación' porque el tema implica reconstruir un tejido social roto...").
            4. **CITA:** Busca una cita textual real (Alem, Yrigoyen, Illia o Alfonsín) que respalde el argumento.

            **SELECTOR VISUAL:**
            Elige el estilo visual: "ÉPICA CALLEJERA", "INSTITUCIONAL SOLEMNE" o "MODERNISMO ABSTRACTO".

            FORMATO JSON:
            1. "frase_radical": Sentencia política desarrollada (La línea discursiva principal).
            2. "nombre_meme": El Concepto/Significante de la Tesis.
            3. "explicacion_meme": La justificación teórica de la conexión entre la frase y el concepto.
            4. "cita_historica": Cita textual real.
            5. "autor_cita": Autor y Año.
            6. "estilo_visual": ELIGE UNO DE LOS 3 ARRIBA.
            7. "prompt_meme": Descripción de la escena visual.
            """

            try:
                # MODELO GPT-4o-MINI
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"Tema: {tema_usuario}. Dame una línea política desarrollada, no un slogan."}
                    ],
                    temperature=0.5 
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # OUTPUTS DE TEXTO
                # Ajustamos un poco el CSS inline aquí para que la letra no sea TAN gigante si la frase es larga
                html_frase = f"""
                <div class="headline-box">
                    <p style="font-size: 1.4rem !important; line-height: 1.3 !important;">"{datos['frase_radical']}"</p>
                </div>
                """
                st.markdown(html_frase, unsafe_allow_html=True)

                html_tesis = f"""
                <div class="thesis-box">
                    <span style="font-size:0.8rem; font-weight:bold; color:#9E9E9E; display:block;">🧬 SIGNIFICANTE ACTIVADO (TESIS)</span>
                    <span style="color:#D32F2F; font-weight:900; font-size:1.4rem; text-transform:uppercase;">{datos['nombre_meme']}</span><br>
                    {datos['explicacion_meme']}
                </div>
                """
                st.markdown(html_tesis, unsafe_allow_html=True)

                html_cita = f"""
                <div class="quote-box">
                    &laquo;{datos['cita_historica']}&raquo;
                    <div style="text-align:right; font-weight:bold; color:#B71C1C; margin-top:5px;">&mdash; {datos['autor_cita']}</div>
                </div>
                """
                st.markdown(html_cita, unsafe_allow_html=True)

                # --- GENERACIÓN DE IMAGEN ---
                if generar_img:
                    st.write("---")
                    st.markdown("**📢 Propaganda Generada por la Máquina:**")
                    with st.spinner(f"Renderizando estética: {datos.get('estilo_visual', 'ÉPICA CALLEJERA')}..."):
                        
                        ESTILOS_UCR = {
                            "ÉPICA CALLEJERA": """
                                Style: Vintage political lithography poster (Argentina 1983), grainy paper texture. 
                                Symbols: Massive crowd wearing white berets (boinas blancas), waving red and white UCR flags. 
                                Vibe: Emotional, democratic mobilization, dusty and historical.
                                """,
                            "INSTITUCIONAL SOLEMNE": """
                                Style: Brutalist or Neoclassical architecture, imposing stone facade of a Congress building. 
                                Symbols: The UCR shield emblem (hammer and quill) subtly engraved in marble or bronze on the wall. No crowds. 
                                Vibe: Serious, heavy, corruption-fighting, unshakeable justice.
                                """,
                            "MODERNISMO ABSTRACTO": """
                                Style: Contemporary Swiss design poster, minimalist typography, clean lines. 
                                Symbols: Abstract geometric deconstruction of the UCR shield. Use of negative space. 
                                Colors: Strict Red (#D32F2F) and White palette. Text 'LISTA 3' integrated artistically. 
                                Vibe: Futuristic, intellectual, clean.
                                """
                        }
                        
                        estilo_elegido = ESTILOS_UCR.get(datos.get('estilo_visual'), ESTILOS_UCR["ÉPICA CALLEJERA"])
                        prompt_final_imagen = f"{estilo_elegido}. Specific Scene: {datos['prompt_meme']}. Main Text overlay in Spanish: '{datos['frase_radical']}'"
                        
                        try:
                            img_res = client.images.generate(
                                model="dall-e-3",
                                prompt=prompt_final_imagen,
                                n=1,
                                size="1024x1024",
                                quality="hd",
                                style="vivid"
                            )
                            st.image(img_res.data[0].url, caption=f"Estética: {datos.get('estilo_visual', 'ÉPICA CALLEJERA')}")
                        except Exception as e:
                            st.warning(f"No se pudo generar la imagen: {e}")

            except Exception as e:
                st.error(f"Error de sistema: {e}")

    else:
        st.warning("Por favor ingresá un tema para consultar a la Máquina.")





