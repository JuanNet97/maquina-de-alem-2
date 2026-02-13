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
    
    /* CAJA 1: LA FRASE RADICAL (Impacto - Recuadro Rojo) */
    .headline-box {
        background-color: #D32F2F !important;
        padding: 25px !important;
        text-align: center !important;
        border-radius: 5px !important;
        margin-bottom: 25px !important;
        border: 2px solid #B71C1C !important;
    }

    /* El texto de adentro (Blanco, Georgia, Negrita) */
    .headline-box p {
        color: #FFFFFF !important; 
        font-family: 'Georgia', serif !important;
        font-weight: bold !important;
        font-size: 1.4rem !important;
        text-transform: none !important;
        margin: 0 !important;
    }

    /* CAJA 2: TESIS (Análisis - Recuadro Blanco) */
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
    
    /* CAJA 3: EVIDENCIA (Cita - Recuadro Gris) */
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
 /* FORZAR ESTILO EN EXPANDERS (Ficha Técnica y Cómo funciona) */
    .streamlit-expanderHeader {
        background-color: white !important;
        color: #333333 !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background-color: white !important;
        color: #333333 !important;
        border: 1px solid #f0f0f0 !important;
        border-top: none !important;
    }

    /* Ajuste para que el texto dentro del expander no se pierda en modo oscuro */
    .stExpander p, .stExpander li, .stExpander span {
        color: #333333 !important;
    }

    /* Color de la flechita del desplegable */
    .stExpander svg {
        fill: #D32F2F !important;
    }
  }
    </style>
    """, unsafe_allow_html=True)
# --- 2. CONEXIÓN CON OPENAI ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ CRÍTICO: No se detectó la API Key. Configurala en 'Secrets'.")
    st.stop()

# --- 3. CARGA DE CONOCIMIENTO (ARREGLO DEFINITIVO) ---
# --- 3. CARGA DE CONOCIMIENTO (ARREGLO DE COMPATIBILIDAD) ---
@st.cache_data
def cargar_conocimiento():
    try:
        # 1. Cargar Tesis
        with open("conocimiento.txt", "r", encoding="utf-8") as f1:
            tesis = f1.read()
            
        # 2. Cargar Discursos (Manejo de error si no existe)
        try:
            with open("discursos.txt", "r", encoding="utf-8") as f2:
                discursos = f2.read()
        except FileNotFoundError:
            discursos = "" # Si no hay archivo, usa vacío.
            
        return tesis, discursos

    except FileNotFoundError:
        st.error("⚠️ Error Crítico: Falta 'conocimiento.txt'.")
        st.stop()

texto_tesis, texto_discursos = cargar_conocimiento()

# COMPATIBILIDAD (Para que no explote si algo viejo busca esta variable)
base_de_conocimiento = texto_tesis

texto_tesis, texto_discursos = cargar_conocimiento()


# --- 4. INTERFAZ DE USUARIO ---

# --- B. CUERPO PRINCIPAL ---
st.title("/// LA MÁQUINA DE ALEM")
st.markdown("### ¿Qué dice el radicalismo sobre...")

st.info("""
**PROYECTO ACADÉMICO EXPERIMENTAL** 

Desarrollado en el marco de la investigación de Juan Ignacio Net como parte de su trabajo final de la **Maestría en Comunicación Política de la Universidad Austral** con fines de divulgación.

Esta API está alimentada exclusivamente por los resultados de la investigación como un ejercicio critico: la idea de que el discurso politico puede ser coherente y a la vez adatarse a las nuevas circunstancias sin perder identidad. 

⚙️ *El modelo se encuentra actualmente en fase de calibración.*
""")

with st.expander("**Ficha técnica y metodología**", expanded=False):
    
    col_a, col_b = st.columns([0.2, 0.8])
    
    with col_b:
        st.markdown("""
        **PROYECTO:** La Máquina de Alem (v2.1)  
        **AUTOR:** Juan Ignacio Net  
        **MAESTRÍA:** Comunicación Política (Univ. Austral)
        """)

    st.divider() 
    
    st.markdown("""
    **DISEÑO DE INVESTIGACIÓN:**
    * **Hipótesis:** La identidad del discurso radical se estructura sobre una matriz de significantes estables ("memes") que garantizan su supervivencia y adaptabilidad histórica.
    * **Metodología:** Análisis cualitativo de discurso sobre un corpus de 8 discursos fundacionales y contemporáneos de la UCR (1890-2023).
    * **Categorías:** 10 significante-memes parametrizados surgidos del análisis discursivo.
    
    ---
    **NOTAS TÉCNICAS:** El modelo utiliza procesamiento de lenguaje natural para clasificar inputs actuales según la lógica interna del discurso radical identificado en la tesis.
    """)
with st.expander("¿Comó funciona **La Maquina de Alem**?", expanded=False):
    st.markdown("""
    
    Esta herramienta opera bajo la matriz teórica de la Tesis. 
    
    **Procedimiento:**
    1.  **Detección:** Identifica cuál de los **Significantes** (categorías resultantes del analisis de la investigacion) se activa con el tema ingresado.
    2.  **Procesamiento:** Genera una postura doctrinaria (Rojo) y una justificación teórica (Blanco).
    3.  **Evidencia:** Rastrea citas textuales en el corpus de discursos cargado en el sistema (Gris).
    """)
tema_usuario = st.text_input("", placeholder="Escribí acá un tema (ej: Educación pública, Inflación, Presupuesto universitario)")

col1, col2 = st.columns([0.65, 0.35])
with col1:
    boton = st.button("HACER HABLAR AL RADICALISMO")
with col2:
    generar_img = st.checkbox("Generar Meme", value=True)

# --- 6. LÓGICA DE PROCESAMIENTO (MODO EXTRACTIVO PURO) ---
# --- 6. LÓGICA DE PROCESAMIENTO (MODO TAXONOMÍA CIENTÍFICA) ---
# --- DEBUG (BORRAR DESPUÉS) ---
# Esto fuerza la carga de variables antes del botón
texto_tesis, texto_discursos = cargar_conocimiento()

if boton:
    if tema_usuario:
        with st.spinner("Procesando matriz de significantes..."):
            
            # 1. TU LISTA DE SIGNIFICANTES (Intacta)
            lista_significantes = """
            1. "Ética Pública": Compromiso con la transparencia, honestidad y rechazo a la corrupción. (Ref: Alem, Illia, Alfonsín, De la Rúa, Manes, Lebensohn).
               -> USAR ESPECÍFICAMENTE PARA: Casos de corrupción, Ficha Limpia, privilegios de la política, sueldos de funcionarios, transparencia en la gestión, honestidad personal.

            2. "Democracia": Defensa activa de las instituciones, participación popular y libertades civiles. (Ref: Alem, Yrigoyen, Illia, Alfonsín, Manes Florentina Gómez Miranda).
               -> USAR ESPECÍFICAMENTE PARA: Voto, fraude, Derechos Humanos, libertad de expresión. (IMPORTANTE: Incluir aquí temas de DERECHOS CIVILES como Divorcio, Matrimonio Igualitario, Género y Feminismo)
          
            3. "Juventud": Interpelación a la juventud como sujeto clave de transformación. (Ref: Alem, Alfonsín, Manes, Lebensohn, Junta Coordinadora NacionaL- Juventud Radical).
               -> USAR ESPECÍFICAMENTE PARA: Estudiantes, Universidad Pública, Reforma del 18, Franja Morada, emigración de jóvenes, futuro, cerebro/ciencia.

            4. "Reparación Nacional": Restaurar un orden social justo y democrático frente a injusticias. (Ref: Yrigoyen, Illia, Alfonsín, Manes, Balbin, Movimiento de Intransigencia y Renovacion).
               -> USAR ESPECÍFICAMENTE PARA: Crisis moral, "sanar" el país, reconstrucción después de una crisis, herencia recibida, recuperar valores perdidos.

            5. "Sacrificio": Compromiso ético y personal extremo por ideales políticos. (Ref: Alem, Yrigoyen, Alfonsín).
               -> USAR ESPECÍFICAMENTE PARA: Austeridad, renunciamientos históricos, militancia desinteresada, "dar la vida", anti-frivolidad.

            6. "Unidad Nacional": Cohesión social y política frente a crisis graves. (Ref: Yrigoyen, Alfonsín, De la Rúa, Manes, Balbín).
               -> USAR ESPECÍFICAMENTE PARA: La Grieta, violencia política, Pacto de Mayo, acuerdos, diálogo, convivencia democrática, "terminar con el odio".

            7. "Justicia Social": Distribución equitativa de recursos y oportunidades. (Ref: Illia, Alfonsín, Manes, Larralde, Federacion Universitaria de Córdoba).
               -> USAR ESPECÍFICAMENTE PARA: (ESTRICTAMENTE ECONÓMICO) Pobreza, Jubilados, Salarios, Inflación, Hambre, Desigualdad de ingresos, Salud Pública, Vivienda.

            8. "Institucionalidad": Respeto a las instituciones, Constitución y legalidad republicana. (Ref: Alvear, Illia, Alfonsín, De la Rúa, Goméz Miranda).
               -> USAR ESPECÍFICAMENTE PARA: Corte Suprema, División de Poderes, Decretos (DNU) vs Leyes, funcionamiento del Congreso, respeto a las reglas de juego.

            9. "Constitucionalismo Ético": Legitimidad basada en la Constitución y valores éticos. (Ref: Illia, Alfonsín, De la Rúa).
               -> USAR ESPECÍFICAMENTE PARA: El Preámbulo, la Constitución como "biblia laica", el Estado de Derecho como valor moral superior, garantías constitucionales.

            10. "Cambio / Renovación": Renovación frente a la corrupción, inmovilismo y decadencia. (Ref: Alem, Alfonsín, De la Rúa, Manes, Junta Coordinadora NacionaL- Juventud Radical, Movimeinto de Renovación y Cambio).
               -> USAR ESPECÍFICAMENTE PARA: Modernización, Progreso, Tecnología, combatir el "atraso", romper el status quo, nuevas ideas vs. viejas prácticas.
            """

            # 2. TU PROMPT (Intacto)
            prompt_sistema = f"""
            Eres "La Máquina de Alem". Tu objetivo es la DIVULGACIÓN CIENTÍFICA de la Tesis de Maestría provista con el maximo rigo conceptual e historico.Tu rol es la gestion del archivo historico de la UCR.
            INSTRUCCIÓN DE RIGOR HISTÓRICO:
            - Antes de asignar un autor a una cita, verifica en la FUENTE 2.
            - Si el texto dice "Manifiesto Liminar", el autor es "Reforma Universitaria (1918)". 
            - NO le asignes frases de la Reforma a Lebensohn ni a Alfonsín por proximidad temática.
            - Si no estás seguro del autor en la FUENTE 2, pon "Registro Histórico UCR".
            
            FUENTE 1 (LA TESIS - El Cerebro):
            {texto_tesis}

            FUENTE 2 (EL CORPUS DE DISCURSOS - La Voz):
            {texto_discursos}

            TUS CATEGORÍAS DE ANÁLISIS (USAR SOLO ESTAS 10):
            {lista_significantes}

            TU MISIÓN PARA EL TEMA: "{tema_usuario}"

            INSTRUCCIONES DE PROCESAMIENTO:

            PASO 1: CLASIFICACIÓN (El Cerebro)
            - Basándote en la FUENTE 1 (Tesis), elige cuál de los 10 significantes aplica mejor.
            Elige el significante MÁS ESPECÍFICO.
            - ⚠️ PROHIBIDO usar "Justicia Social" por defecto. Úsalo SOLO si el tema es estrictamente económico o de pobreza

            PASO 2: REDACCIÓN POLÍTICA (Recuadro Rojo)
            - Redacta una sentencia política de 2 o 3 oraciones. Tono doctrinario con la cadencia de la oratoria radical (estilo Alfonsín, Illia o Alem).
            - TONO: Épico, ético, austero y republicano. Evita palabras modernas como "gestión" o "management"; usa "misión", "causa", "civismo" o "reparación".
            - ESTRUCTURA: 
            1. Empieza con una afirmación de principios sobre el tema que no sea simpre "la causa..." seguido del input o algun significante. 
            2. Sigue con la exigencia ética que el radicalismo impone frente a esa realidad.
            3. Termina con una sentencia breve y contundente que cierre la postura.
            - REGLA DE ORO: Debe sonar como algo que se podría decir en un atril de madera o en una plaza, no en una oficina.

            PASO 3: BÚSQUEDA SEMÁNTICA DE EVIDENCIA (MODO CAZADOR)
            - Tu prioridad absoluta es encontrar una cita en la FUENTE 2.
            - 1ra Opción: Una cita que mencione el tema "{tema_usuario}" o algo relacionado.
            - 2da Opción (FALLBACK): Si el tema no está literal, buscá la cita más ICONICA y potente de la FUENTE 2 que represente el "Significante" elegido. 
            - No te rindas. Si el significante es "Ética Pública", buscá la frase más fuerte de Alem o Illia sobre la honestidad, aunque no hablen del tema exacto del usuario.
            -⚠️ METADATOS: Identifica el autor y el año REAL que figuran en la FUENTE 2.
            - Si el año no figura en el texto, NO LO INVENTES. Poné solo el nombre del autor o "Registro histórico".

            PASO 4: JUSTIFICACIÓN TEÓRICA (Recuadro Blanco)
            - Explica la conexión entre el tema y el significante usando la lógica de la FUENTE 1 (Tesis).

            PASO 5: EVIDENCIA (Recuadro Gris)
            - Extrae el fragmento literal encontrado en la FUENTE 2.
            - ⚠️ NUNCA inventes una cita. Si realmente no hay nada en la Fuente 2 (lo cual es raro), solo ahí devuelve "null".

            FORMATO JSON:
            {{
                "frase_radical": "Texto de 2 o 3 oraciones...",
                "nombre_meme": "NOMBRE EXACTO DEL SIGNIFICANTE",
                "explicacion_meme": "Justificación teórica basada en Fuente 1...",
                "cita_historica": "Texto literal encontrado en Fuente 2 O null",
                "autor_cita": "Nombre del Autor (Año) - Solo si el año está en la Fuente 2",
                "estilo_visual": "ÉPICA CALLEJERA, INSTITUCIONAL SOLEMNE o MODERNISMO ABSTRACTO",
                "prompt_meme": "Descripción visual"
            }}
            """

            try:
                # 3. LLAMADA A LA API (Indentada correctamente)
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"Tema: {tema_usuario}"}
                    ],
                    temperature=0.1
                )

                contenido_crudo = respuesta.choices[0].message.content
                datos = json.loads(contenido_crudo)

                # --- 4. SALIDA VISUAL (Con tu diseño y tipografías originales) ---
                
                # Recuadro Rojo: El único con Georgia Blanca forzada como pediste
                frase = datos.get("frase_radical", "Analizando...")
                st.markdown(f"""
                <div class="headline-box">
                    <p style="color: #FFFFFF !important; font-family: 'Georgia', serif !important; font-weight: bold !important; font-size: 1.4rem !important; text-transform: none !important; margin: 0; line-height: 1.4;">
                        "{frase}"
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Recuadro Blanco: Respeta tus clases CSS originales
                nombre_sig = datos.get("nombre_meme", "Significante")
                explicacion = datos.get("explicacion_meme", "")
                st.markdown(f"""
                <div class="thesis-box">
                    <span class="thesis-label">SIGNIFICANTE ACTIVADO</span>
                    <span class="meme-name">{nombre_sig}</span>
                    <div>{explicacion}</div>
                </div>
                """, unsafe_allow_html=True)

                # Recuadro Gris: Respeta tus clases CSS originales
                cita = datos.get("cita_historica")
                if cita and cita != "null":
                    autor_anio = datos.get("autor_cita", "Registro histórico")
                    st.markdown(f"""
                    <div class="quote-box">
                        &laquo;{cita}&raquo;
                        <div class="quote-author">— {autor_anio}</div>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error de procesamiento: {e}")
              # --- PROCESAMIENTO BLINDADO DE JSON ---
                import json
                import re

                # 1. LIMPIEZA: Usamos la variable correcta 'respuesta' y el formato de OpenAI
                texto_limpio = respuesta.choices[0].message.content
                
                # Limpiamos los bloques de código si la IA los mandó
                texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
                
                # 2. PARSEO
                import json
                resultado_json = json.loads(texto_limpio)
                
                # 3. ASIGNACIÓN CRÍTICA (Para que el resto del código funcione)
                datos = resultado_json

                
                # 3. EXTRACCIÓN SEGURA (El secreto para que no explote)
                # Usamos .get() en lugar de corchetes []. Si no existe, pone un texto por defecto.
                
                frase_radical = resultado_json.get("frase_radical", "⚠️ La Máquina está pensando... (Error de formato, intentá de nuevo).")
                nombre_meme = resultado_json.get("nombre_meme", "Análisis Radical")
                explicacion_meme = resultado_json.get("explicacion_meme", "No se pudo procesar la explicación técnica.")
                
                cita_historica = resultado_json.get("cita_historica", "null")
                autor_cita = resultado_json.get("autor_cita", "")
                prompt_meme = resultado_json.get("prompt_meme", "Poster político estilo radicalismo clásico")

                # --- FIN DEL PROCESAMIENTO ---

                # AHORA SÍ, MOSTRÁ LOS RESULTADOS (Tu código de visualización sigue acá abajo...)
                # st.markdown(f"### {frase_radical}") ... etc
                # --- OUTPUT VISUAL ---

                # 1. Línea Discursiva (Rojo)
              # 1. LÍNEA DISCURSIVA (RECUADRO ROJO)
                # El .get() evita que la app muera si la IA no manda la clave exacta
                frase_radical = datos.get("frase_radical", "La Máquina está procesando el pensamiento...")
                
                html_frase = f"""
                <div class="headline-box">
                    <p style="color: #FFFFFF !important; font-family: 'Georgia', serif !important; font-weight: bold !important; font-size: 1.4rem !important; text-transform: none !important; margin: 0; line-height: 1.3;">
                        "{frase_radical}"
                    </p>
                </div>
                """
                st.markdown(html_frase, unsafe_allow_html=True)

                # 2. EXPLICACIÓN DEL SIGNIFICANTE (RECUADRO BLANCO)
                nombre_meme = datos.get("nombre_meme", "Significante")
                explicacion = datos.get("explicacion_meme", "Analizando matriz discursiva...")
                
                html_tesis = f"""
                <div class="thesis-box">
                    <span class="thesis-label">SIGNIFICANTE ACTIVADO (TESIS)</span>
                    <span style="color:#D32F2F; font-weight:900; font-size:1.4rem; text-transform:uppercase; display:block; margin-bottom:10px;">{nombre_meme}</span>
                    <div style="color: #333333 !important;">{explicacion}</div>
                </div>
                """
                st.markdown(html_tesis, unsafe_allow_html=True)

                # 3. Cita Histórica (Solo si es real)
                cita = datos.get('cita_historica')
                if cita and cita != "null" and len(cita) > 10:
                    html_cita = f"""
                    <div class="quote-box">
                        &laquo;{cita}&raquo;
                        <div style="text-align:right; font-weight:bold; color:#B71C1C; margin-top:5px;">&mdash; {datos.get('autor_cita', '')}</div>
                    </div>
                    """
                    st.markdown(html_cita, unsafe_allow_html=True)
                else:
                    # Mensaje de transparencia si no hay cita
                    st.caption("📝 *El archivo de tesis no contiene una cita textual directa para vincular este tema específico.*")

                # --- GENERACIÓN DE IMAGEN ---
                if generar_img:
                    st.write("---")
                    st.markdown("**📢 Propaganda Generada por la Máquina:**")
                    with st.spinner(f"Renderizando estética: {datos.get('estilo_visual', 'ÉPICA CALLEJERA')}..."):
                        
                        ESTILOS_UCR = {
                            "ÉPICA CALLEJERA": "Vintage political lithography poster (Argentina 1983), grainy paper texture. Massive crowd, white berets (boinas blancas), waving red and white UCR flags. Emotional.",
                            "INSTITUCIONAL SOLEMNE": "Brutalist architecture, imposing stone facade of Congress. UCR shield emblem (hammer and quill) engraved in marble. Serious, heavy.",
                            "MODERNISMO ABSTRACTO": "Contemporary Swiss design poster, minimalist typography. Abstract geometric deconstruction of UCR shield. Strict Red (#D32F2F) and White palette."
                        }
                        
                        estilo = ESTILOS_UCR.get(datos.get('estilo_visual'), ESTILOS_UCR["ÉPICA CALLEJERA"])
                        prompt_img = f"{estilo}. Scene: {datos['prompt_meme']}. Text: '{datos['nombre_meme']}'"
                        
                        try:
                            img_res = client.images.generate(model="dall-e-3", prompt=prompt_img, n=1, size="1024x1024", quality="hd", style="vivid")
                            st.image(img_res.data[0].url, caption=f"Estética: {datos.get('estilo_visual')}")
                        except Exception as e:
                            st.warning(f"Error imagen: {e}")

            except Exception as e:
                st.error(f"Error de sistema: {e}")

    else:
        st.warning("Por favor ingresá un tema para consultar a la Máquina.")
































































