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

# --- 6. LÓGICA DE PROCESAMIENTO ---
if boton:
    if tema_usuario:
        with st.spinner("Procesando análisis de la tesis..."):
            
            # --- PROMPT CORREGIDO: USAR LA DATA QUE SÍ ESTÁ ---
            prompt_sistema = f"""
            Eres "La Máquina de Alem". Tu cerebro es ESTRICTAMENTE el texto de la Tesis de Maestría provista.
            
            TU BASE DE DATOS:
            {base_de_conocimiento}

            INSTRUCCIONES DE PROCESAMIENTO:
            El usuario ingresa: "{tema_usuario}".
            
            1. **LÍNEA DISCURSIVA (Recuadro Rojo):**
               - NO uses slogans de marketing.
               - Redacta una **sentencia política completa y desarrollada** (tipo párrafo de discurso).
               - Construye esta frase emulando la retórica y los conceptos (Significantes) que la Tesis analiza.
               - Ejemplo de tono buscado: "La democracia no es un pacto de silencio, sino la ética de la responsabilidad frente a un régimen que atropella las instituciones."
            
            2. **EL SIGNIFICANTE (Concepto):**
               - Identifica qué categoría teórica de la Tesis (ej: La Reparación, La Ética, El Régimen) se activa con este tema.

            3. **JUSTIFICACIÓN TÉCNICA:**
               - Explica brevemente por qué la frase que generaste arriba responde a ese Significante según el análisis de la tesis.

            4. **EVIDENCIA TEXTUAL (La Cita):**
               - Busca en el texto provisto algún **fragmento de discurso** que haya sido analizado.
               - Extrae ese fragmento TEXTUAL.
               - Si el análisis cita a Alem, Yrigoyen, Illia o Alfonsín, usa esa parte.

            **SELECTOR VISUAL:**
            Elige: "ÉPICA CALLEJERA", "INSTITUCIONAL SOLEMNE" o "MODERNISMO ABSTRACTO".

            FORMATO JSON:
            1. "frase_radical": La línea discursiva desarrollada.
            2. "nombre_meme": El Significante de la Tesis.
            3. "explicacion_meme": Justificación teórica.
            4. "cita_historica": El fragmento textual extraído de la tesis.
            5. "autor_cita": Autor y Año del fragmento.
            6. "estilo_visual": ELIGE UNO DE LOS 3 ARRIBA.
            7. "prompt_meme": Descripción visual de la escena.
            """

            try:
                # Usamos temperatura 0.4 para que sea creativo al redactar la línea política
                # pero estricto al buscar la información en la tesis.
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"Tema: {tema_usuario}. Genera línea política basada en el análisis."}
                    ],
                    temperature=0.4 
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # OUTPUTS DE TEXTO
                
                # CSS Inline para asegurar que la frase larga se lea bien
                html_frase = f"""
                <div class="headline-box">
                    <p style="font-size: 1.3rem !important; line-height: 1.4 !important; font-weight: 700 !important; font-family: 'Georgia', serif !important; text-transform: none !important;">
                        "{datos['frase_radical']}"
                    </p>
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
                            "ÉPICA CALLEJERA": "Vintage political lithography poster (Argentina 1983), grainy paper texture. Massive crowd, white berets (boinas blancas), waving red and white UCR flags. Emotional, democratic mobilization.",
                            "INSTITUCIONAL SOLEMNE": "Brutalist or Neoclassical architecture, imposing stone facade of a Congress building. The UCR shield emblem (hammer and quill) subtly engraved in marble. Serious, heavy, corruption-fighting vibe.",
                            "MODERNISMO ABSTRACTO": "Contemporary Swiss design poster, minimalist typography, clean lines. Abstract geometric deconstruction of the UCR shield. Negative space. Strict Red (#D32F2F) and White palette."
                        }
                        
                        estilo_elegido = ESTILOS_UCR.get(datos.get('estilo_visual'), ESTILOS_UCR["ÉPICA CALLEJERA"])
                        
                        # Usamos 'nombre_meme' (el concepto) para el texto de la imagen, que es más corto
                        prompt_final_imagen = f"{estilo_elegido}. Specific Scene: {datos['prompt_meme']}. Text overlay: '{datos['nombre_meme']}'"
                        
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



