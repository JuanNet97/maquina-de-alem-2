import streamlit as st
from openai import OpenAI
import json

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="La Máquina de Alem", page_icon="🇦🇷", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; border-top: 20px solid #D32F2F; }
    h1 { color: #D32F2F; font-family: 'Helvetica', sans-serif; font-weight: 900; text-transform: uppercase; margin-bottom: 0px; }
    
    /* CAJA 1: FRASE */
    .headline-box {
        background-color: #D32F2F; color: white; padding: 25px; text-align: center;
        font-family: 'Arial Black', sans-serif; font-size: 1.6rem; text-transform: uppercase;
        border-radius: 4px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* CAJA 2: TESIS */
    .thesis-box {
        background-color: #fff; padding: 20px; border-left: 8px solid #212121;
        font-family: 'Georgia', serif; color: #333; margin-bottom: 15px;
    }
    .thesis-label { font-size: 0.85rem; font-weight: bold; color: #757575; text-transform: uppercase; display: block; margin-bottom: 10px; letter-spacing: 1px; }
    .meme-name { color: #D32F2F; font-weight: 900; font-size: 1.2rem; text-transform: uppercase; }
    
    /* CAJA 3: CITA */
    .quote-box {
        background-color: #eceff1; padding: 15px; font-style: italic; border-right: 6px solid #B71C1C;
        color: #455a64; margin-bottom: 20px; font-size: 0.95rem;
    }
    .quote-author { text-align: right; font-weight: bold; color: #B71C1C; font-size: 0.8rem; margin-top: 5px; text-transform: uppercase; }

    .stButton>button { background-color: #212121; color: white; border: none; font-weight: bold; width: 100%; padding: 12px; text-transform: uppercase; transition: 0.3s; }
    .stButton>button:hover { background-color: #424242; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ Error: Falta API Key.")
    st.stop()

# --- 3. CARGA DE CONOCIMIENTO ---
@st.cache_data
def cargar_conocimiento():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            # Leemos hasta 70k caracteres para que entren más discursos
            return f.read()[:70000] 
    except FileNotFoundError:
        st.error("⚠️ Error: Falta 'conocimiento.txt'.")
        st.stop()

base_de_conocimiento = cargar_conocimiento()

# --- 4. INTERFAZ ---
st.title("/// LA MÁQUINA DE ALEM")
st.markdown("### ¿Qué dice el radicalismo sobre...?")
st.info("Ingresá un tema. El sistema analizará la Tesis y el Archivo Histórico para generar una respuesta.")

tema_usuario = st.text_input("", placeholder="Ej: El financiamiento universitario, la corrupción...")

col1, col2 = st.columns([0.65, 0.35])
with col1:
    boton = st.button("HACER HABLAR AL RADICALISMO")
with col2:
    generar_img = st.checkbox("Generar Meme", value=True)

# --- 5. PROCESAMIENTO ---
if boton:
    if tema_usuario:
        with st.spinner("Procesando Archivo Histórico..."):
            
            # --- PROMPT BLINDADO ---
            prompt = f"""
            Eres "La Máquina de Alem". Tu base de datos es:
            --- INICIO TEXTO ---
            {base_de_conocimiento}
            --- FIN TEXTO ---

            TAREA:
            El usuario pregunta sobre: "{tema_usuario}".
            
            REGLAS ESTRICTAS:
            1. FECHAS REALES: Al citar, extrae el AÑO que figura en el encabezado del discurso en el texto provisto. Si no está seguro, no inventes fecha.
            2. FORMATO MEME: Identifica qué concepto de la tesis aplica (ej: La Reparación, Ética, etc.).

            FORMATO JSON OBLIGATORIO:
            1. "frase_radical": Slogan político contundente.
            2. "nombre_meme": Nombre del concepto de la tesis.
            3. "explicacion_meme": Justificación teórica breve.
            4. "cita_historica": Cita textual exacta.
            5. "autor_cita": Autor y Año real (extraído del texto).
            6. "prompt_meme": Descripción visual para el meme.
            """

            try:
                # 1. GPT (Texto)
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": tema_usuario}
                    ],
                    temperature=0.5
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # OUTPUTS TEXTO
                st.markdown(f"""
                <div class="headline-box">
                    "{datos['frase_radical']}"
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="thesis-box">
                    <span class="thesis-label">🧬 SIGNIFICANTE DE LA TESIS</span>
                    <span class="meme-name">{datos['nombre_meme']}</span><br>
                    {datos['explicacion_meme']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="quote-box">
                    «{datos['cita_historica']}»
                    <div class="quote-author">— {datos['autor_cita']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 2. DALL-E (Imagen con Símbolos UCR)
                if generar_img:
                    st.write("**Representación Gráfica:**")
                    with st.spinner("Renderizando simbología radical..."):
                        
                        # AQUÍ ESTÁ LA INYECCIÓN DE SÍMBOLOS UCR
                        simbologia_ucr = "symbolism of Argentine Radical Civic Union, white berets (boinas blancas), red and white flags, massive political rally style, vintage aesthetic 1983"
                        
                        prompt_final_imagen = f"Political poster graphic design, {datos['prompt_meme']}, {simbologia_ucr}, text in Spanish: '{datos['frase_radical']}', colors red white and black, high contrast propaganda style."
                        
                        try:
                            img = client.images.generate(
                                model="dall-e-3",
                                prompt=prompt_final_imagen,
                                n=1,
                                size="1024x1024"
                            )
                            st.image(img.data[0].url, caption=f"Concepto: {datos['frase_radical']}")
                        except Exception as e:
                            st.warning(f"No se pudo generar imagen: {e}")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Escribí un tema.")

