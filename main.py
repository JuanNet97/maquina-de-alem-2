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
if boton:
    if tema_usuario:
        with st.spinner("Procesando Archivo Histórico completo..."):
            
            # --- PROMPT PARA GPT-4o-MINI ---
            prompt_sistema = f"""
            Eres "La Máquina de Alem", la conciencia histórica de la UCR.
            
            TU CEREBRO (Base de Conocimiento):
            --- INICIO TEXTO ---
            {base_de_conocimiento}
            --- FIN TEXTO ---

            TU MISIÓN:
            El usuario ingresa un tema actual. Responde basándote en la Tesis y los Discursos.

            REGLAS DE BÚSQUEDA (IMPORTANTE):
            1. **VARIEDAD OBLIGATORIA:** Tienes discursos de Alem, Yrigoyen, Larralde, Illia, Balbín y Alfonsín. NO CITES SIEMPRE A ALFONSÍN. Busca activamente citas de los fundadores o de la intransigencia si aplican.
            2. **Cita Textual:** Extrae la frase exacta y el AÑO del texto provisto. No inventes.
            3. **Significante:** Relaciona el tema con un concepto de la tesis.

            FORMATO JSON:
            1. "frase_radical": Slogan político contundente.
            2. "nombre_meme": Concepto de la tesis.
            3. "explicacion_meme": Justificación teórica.
            4. "cita_historica": Cita textual (Priorizar autores distintos a Alfonsín si es posible).
            5. "autor_cita": Autor y Año.
            6. "prompt_meme": Descripción visual para poster político.
            """

            try:
                # MODELO GPT-4o-MINI (Rápido, Barato, Gran Memoria)
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"El tema es: {tema_usuario}. (Busca variedad histórica en la cita)."}
                    ],
                    temperature=0.7 
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # OUTPUTS (Con corrección HTML para móvil)
                st.markdown(f"""
                <div class="headline-box">
                    <p>"{datos['frase_radical']}"</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="thesis-box">
                    <span style="font-size:0.8rem; font-weight:bold; color:#9E9E9E; display:block;">SIGNIFICANTE ACTIVADO (TESIS)</span>
                    <span style="color:#D32F2F; font-weight:900; font-size:1.4rem; text-transform:uppercase;">{datos['nombre_meme']}</span><br>
                    {datos['explicacion_meme']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="quote-box">
                    &laquo;{datos['cita_historica']}&raquo;
                    <div class="quote-author">- {datos['autor_cita']}</div>
                </div>
                """, unsafe_allow_html=True)

                # IMAGEN
               # --- BLOQUE DE IMAGEN REFINADO ---
                if generar_img:
                    st.write("---")
                    st.markdown("**📢 Propaganda Generada por la Máquina:**")
                    with st.spinner("Inyectando simbología partidaria en DALL-E..."):
                        
                        # --- NUEVAS INSTRUCCIONES VISUALES DE ALTA PRECISIÓN ---
                        # 1. Estilo: Litografía política vintage, textura de papel viejo y granulado.
                        # 2. Colores: Estricto rojo, blanco y tinta negra. Alto contraste.
                        # 3. Símbolos Clave: Boinas blancas en masa, banderas rojas y blancas de la UCR.
                        # 4. Elementos Institucionales: Escudo de la UCR (sol naciente, martillo y pluma), texto "LISTA 3".
                        # 5. Atmósfera: Épica de movilización callejera democrática (estilo 1983).
                        
                        simbologia_obligatoria = """
                        Vintage political propaganda poster style from Argentina (1983 era), lithography texture on grainy paper. 
                        Strict Red and White color palette with black ink contrast. 
                        Key elements: Massive crowd wearing white berets (boinas blancas), numerous red and white UCR flags, 
                        iconography of the UCR shield (rising sun, hammer and quill pen emblem), "LISTA 3" text on banners. 
                        Atmosphere of epic democratic mobilization.
                        """
                        
                        # Combinamos: Simbología obligatoria + Descripción del concepto + El texto a incluir
                        prompt_final_imagen = f"{simbologia_obligatoria}. Poster depicting: {datos['prompt_meme']}. Big bold text overlay in Spanish: '{datos['frase_radical']}'"
                        
                        try:
                            # Usamos 'vivid' para colores más potentes y 'hd' para que se lean mejor los textos
                            img_res = client.images.generate(
                                model="dall-e-3",
                                prompt=prompt_final_imagen,
                                n=1,
                                size="1024x1024",
                                quality="hd", 
                                style="vivid" 
                            )
                            st.image(img_res.data[0].url, caption=f"Concepto Visual: {datos['frase_radical']}")
                        except Exception as e:
                            st.warning(f"No se pudo generar la imagen (Posible error de API o contenido): {e}")

            except Exception as e:
                st.error(f"Error de sistema: {e}")

    else:
        st.warning("Por favor ingresá un tema para consultar a la Máquina.")





