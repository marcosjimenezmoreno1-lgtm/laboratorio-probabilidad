import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import time
from datetime import datetime

# Configuracion basica
st.set_page_config(
    page_title="Laboratorio de Probabilidad",
    page_icon="🎲",
    layout="wide"
)

# --- Funciones auxiliares sencillas ---

def preparar_grafica(ax):
    # para que las graficas de matplotlib no queden tan feas por defecto
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

# --------------------------------------------------
# ENRUTAMIENTO (Navegación entre pestañas)
# --------------------------------------------------
# Lo vi en un tutorial: leemos un parámetro de la URL para saber qué mostrar.
# Así podemos poner un enlace HTML con target="_blank" para abrir una pestaña nueva.
modo = st.query_params.get("modo", "actividades")

if modo == "actividades":
    
    st.title("📚 Actividades de probabilidad")
    st.write("Resuelve estas actividades. Necesitarás usar el simulador para contestar.")
    
    # Botón casero hecho con HTML para forzar la apertura en otra pestaña
    st.markdown(
        """
        <a href="?modo=lab" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #4C72B0; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin-bottom: 20px;">
            🚀 Abrir el Laboratorio en una pestaña nueva
        </a>
        """, 
        unsafe_allow_html=True
    )
    
    st.warning("Si recargas esta página se borrarán tus respuestas. Descarga el archivo al final.")

    actividades = [
        {
            "titulo": "Actividad 1. ¿Es justa una moneda?",
            "descripcion": (
                "Una empresa fabrica monedas y asegura que todas están "
                "equilibradas, es decir, que tienen la misma probabilidad de "
                "salir cara que cruz. Sin embargo, algunos alumnos creen que, "
                "al lanzar una moneda varias veces, uno de los resultados "
                "puede aparecer con mucha más frecuencia que el otro."
            ),
            "preguntas": [
                "Si lanzamos una moneda equilibrada, ¿cuál es la probabilidad de obtener cara? ¿Y de obtener cruz?",
                "Utiliza el simulador para lanzar una moneda 10 veces. ¿Cuántas veces ha salido cara? ¿Y cruz? ¿Han aparecido el mismo número de veces?",
                "Repite el experimento realizando 50, 100, 500 y 1000 lanzamientos. Calcula la frecuencia relativa de cada resultado y representa cómo va cambiando a medida que aumenta el número de lanzamientos.",
                "¿Qué ocurre con las frecuencias relativas cuando aumenta el número de lanzamientos? ¿Se aproximan a las probabilidades teóricas? ¿Significa esto que acabarán siendo exactamente iguales?",
                "Modifica la probabilidad de obtener cara al 70 % y repite el experimento. ¿Cómo cambian los resultados? ¿Serías capaz de descubrir si una moneda está trucada realizando solamente 10 lanzamientos?",
                "Un alumno afirma que, si al lanzar una moneda han salido cinco caras seguidas, en el siguiente lanzamiento es más probable que salga cruz. ¿Es correcta su afirmación? Razona tu respuesta."
            ]
        },
        {
            "titulo": "Actividad 2. El misterio de los dos dados",
            "descripcion": (
                "En muchos juegos de mesa se utilizan dos dados y se obtienen "
                "puntos dependiendo de la suma de los resultados. Un grupo de "
                "amigos quiere diseñar un juego y necesita saber qué sumas "
                "tienen más posibilidades de aparecer."
            ),
            "preguntas": [
                "Al lanzar dos dados, ¿cuáles son las sumas que se pueden obtener? ¿Cuál crees que aparecerá con mayor frecuencia?",
                "Utiliza el simulador para realizar 100 lanzamientos de dos dados y anota cuántas veces aparece cada suma.",
                "Repite el experimento realizando 500 y 1000 lanzamientos. ¿Cambian mucho los resultados? ¿Coinciden con lo que habías pensado inicialmente?",
                "¿De cuántas formas diferentes se puede obtener una suma de 7? ¿Y una suma de 10? Utiliza los posibles resultados de los dos dados para calcular sus probabilidades.",
                "Un jugador propone ganar si la suma de los dados es 7, mientras que otro propone ganar si la suma es 10. ¿Tienen ambos la misma probabilidad de ganar? ¿Qué jugador tiene ventaja?",
                "Si quisieras diseñar un juego en el que dos jugadores tuvieran las mismas posibilidades de ganar, ¿qué condiciones establecerías? Comprueba tu propuesta utilizando el simulador."
            ]
        },
        {
            "titulo": "Actividad 3. ¿Influye devolver las bolas a la urna?",
            "descripcion": (
                "En una urna hay 4 bolas rojas y 6 bolas azules. Se extraen "
                "dos bolas consecutivamente y se quiere estudiar la probabilidad "
                "de obtener bolas de cada color. Para ello, se realizarán dos "
                "experimentos: en el primero se devuelve la primera bola antes "
                "de extraer la segunda y, en el segundo, no se devuelve."
            ),
            "preguntas": [
                "¿Cuál es la probabilidad de extraer una bola roja en la primera extracción? ¿Y una azul?",
                "Utiliza el simulador para realizar varias extracciones con reemplazamiento. ¿Qué resultados obtienes al extraer dos bolas? ¿Y si realizas el experimento sin reemplazamiento?",
                "Calcula la probabilidad de obtener dos bolas rojas en cada uno de los experimentos. ¿Se obtiene el mismo resultado cuando se devuelve la primera bola que cuando no se devuelve?",
                "¿Cuál es la probabilidad de obtener dos bolas de distinto color en cada caso? ¿Y la de obtener al menos una bola azul?",
                "Representa los dos experimentos mediante un diagrama de árbol. ¿Qué diferencias observas? ¿Por qué cambia la probabilidad de la segunda extracción cuando no se devuelve la primera bola?",
                "Ahora imagina que tienes una urna cuya composición desconoces. Realiza varias extracciones y, a partir de los resultados, intenta averiguar cuántas bolas de cada color contiene. ¿Podrías conocer su composición exacta realizando únicamente unas pocas extracciones?"
            ]
        },
        {
            "titulo": "Actividad 4. Diseña tu propio juego de azar",
            "descripcion": (
                "Un centro educativo quiere organizar una feria matemática en "
                "la que los alumnos preparen diferentes juegos de azar utilizando "
                "monedas, dados y urnas. Para que los juegos sean interesantes, "
                "sus reglas deben estar bien definidas y las probabilidades de "
                "ganar deben poder calcularse."
            ),
            "preguntas": [
                "Escoge uno de los experimentos disponibles en el laboratorio y diseña un juego en el que intervenga el azar. Explica sus reglas e indica qué resultados permiten ganar y cuáles hacen perder.",
                "Antes de utilizar el simulador, ¿qué probabilidad crees que tiene un jugador de ganar? ¿Consideras que el juego es justo?",
                "Calcula la probabilidad de ganar y la de perder. ¿Coinciden con lo que habías pensado inicialmente?",
                "Utiliza el simulador para realizar un gran número de partidas. ¿Qué porcentaje de veces se gana? Compara los resultados obtenidos con las probabilidades que has calculado.",
                "Modifica alguna de las reglas para cambiar las posibilidades de ganar. ¿Qué has cambiado? ¿Ha aumentado o disminuido la probabilidad de victoria?",
                "Explica al resto de la clase cómo funciona tu juego, qué probabilidades intervienen y por qué consideras que es justo o injusto."
            ]
        }
    ]

    # Para que si escriben algo no se pierda la sesión
    def marcar_cambio():
        st.session_state["cambios"] = True

    # Generamos los campos de texto
    for i, act in enumerate(actividades):
        with st.expander(act["titulo"], expanded=True):
            st.write(act["descripcion"]) 
            for j, preg in enumerate(act["preguntas"]):
                st.write(f"**{j+1}.** {preg}")
                st.text_area("Respuesta:", key=f"resp_{i}_{j}", on_change=marcar_cambio)

    st.markdown("---")
    st.subheader("Guardar respuestas")
    
    col1, col2 = st.columns(2)
    nombre = col1.text_input("Tu nombre completo:")
    curso = col2.text_input("Curso:")

    if st.button("Generar archivo para entregar", type="primary"):
        # montamos el texto a mano, sin librerias raras
        texto_final = f"ALUMNO: {nombre}\nCURSO: {curso}\nFECHA: {datetime.now().strftime('%d/%m/%Y')}\n\n"
        texto_final += "="*40 + "\nRESPUESTAS\n" + "="*40 + "\n\n"
        
        for i, act in enumerate(actividades):
            texto_final += f"--- {act['titulo'].upper()} ---\n"
            for j, preg in enumerate(act["preguntas"]):
                respuesta = st.session_state.get(f"resp_{i}_{j}", "(Sin responder)")
                texto_final += f"P: {preg}\nR: {respuesta}\n\n"
        
        st.success("¡Archivo generado! Pulsa abajo para descargar.")
        st.download_button(
            label="Descargar mis respuestas (.txt)",
            data=texto_final,
            file_name=f"Practica_Probabilidad_{nombre.replace(' ', '_')}.txt",
            mime="text/plain"
        )


# --------------------------------------------------
# ZONA DEL LABORATORIO (Se abre en la otra pestaña)
# --------------------------------------------------
elif modo == "lab":
    st.sidebar.title("Opciones")
    
    experimento = st.sidebar.selectbox(
        "Elige qué experimento hacer:",
        ["Lanzamiento de monedas", "Lanzamiento de dados", "Extracción de bolas"]
    )
    
    st.title("🧪 Laboratorio de Probabilidad")
    st.markdown("---")

    # ==========================================
    # EXPERIMENTO 1: MONEDAS
    # ==========================================
    if experimento == "Lanzamiento de monedas":
        st.header("🟡 Lanzamiento de monedas")
        
        c1, c2 = st.columns(2)
        n_lanzamientos = c1.number_input("Número de lanzamientos", min_value=10, max_value=10000, value=100)
        prob_cara = c2.slider("Probabilidad de sacar cara (%)", 0, 100, 50)
        
        if st.button("Lanzar moneda"):
            with st.spinner('Lanzando...'):
                time.sleep(0.8) # para darle un toque de que está "pensando"
                
                # Simulamos con distribucion binomial
                resultados = np.random.binomial(1, prob_cara / 100, size=n_lanzamientos)
                caras = int(np.sum(resultados))
                cruces = n_lanzamientos - caras
                
                frecuencia_rel = caras / n_lanzamientos
                # para la grafica de lineas
                acumuladas = np.cumsum(resultados) / np.arange(1, n_lanzamientos + 1)
                
                st.success(f"¡Experimento completado! Se han lanzado {n_lanzamientos} monedas.")
                
                col_res1, col_res2, col_res3 = st.columns(3)
                col_res1.metric("Caras", caras)
                col_res2.metric("Cruces", cruces)
                col_res3.metric("Frec. Relativa (Caras)", f"{frecuencia_rel:.3f}")
                
                st.subheader("Evolución de la frecuencia relativa")
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(acumuladas, label="Frecuencia experimental", color="blue")
                ax.axhline(y=prob_cara/100, color="orange", linestyle="--", label="Probabilidad teórica")
                ax.set_ylim(-0.1, 1.1)
                ax.set_xlabel("Nº de lanzamientos")
                ax.set_ylabel("Frecuencia")
                preparar_grafica(ax)
                ax.legend()
                st.pyplot(fig)


    # ==========================================
    # EXPERIMENTO 2: DADOS
    # ==========================================
    elif experimento == "Lanzamiento de dados":
        st.header("🎲 Lanzamiento de dados")
        
        c1, c2 = st.columns(2)
        num_dados = c1.selectbox("Número de dados a lanzar a la vez", [1, 2, 3], index=1)
        simulaciones = c2.number_input("Número de tiradas", min_value=10, max_value=10000, value=1000)
        
        if st.button("Lanzar dados"):
            with st.spinner('Lanzando dados...'):
                time.sleep(0.8)
                
                # Generamos matriz de tiradas (filas=simulaciones, columnas=num_dados)
                tiradas = np.random.randint(1, 7, size=(simulaciones, num_dados))
                sumas = np.sum(tiradas, axis=1)
                
                # Calculo teorico usando convolucion (lo vi en un foro de mates en python, sirve para n dados)
                dist_teorica = np.array([1.0])
                for _ in range(num_dados):
                    dist_teorica = np.convolve(dist_teorica, np.ones(6) / 6)
                
                valores_posibles = np.arange(num_dados, 6 * num_dados + 1)
                
                frec_absolutas = [np.sum(sumas == v) for v in valores_posibles]
                frec_relativas = np.array(frec_absolutas) / simulaciones
                
                st.success("¡Tiradas completadas!")
                
                fig, ax = plt.subplots(figsize=(10, 4))
                x = np.arange(len(valores_posibles))
                width = 0.4
                
                ax.bar(x - width/2, frec_relativas, width, label="Experimental", color="#4C72B0")
                ax.bar(x + width/2, dist_teorica, width, label="Teórica", color="#DD8452")
                ax.set_xticks(x)
                ax.set_xticklabels(valores_posibles)
                
                preparar_grafica(ax)
                ax.legend()
                
                st.pyplot(fig)
                
                # Tabla resumen
                st.write("**Tabla comparativa:**")
                df = pd.DataFrame({
                    "Suma": valores_posibles,
                    "Frecuencia Abs": frec_absolutas,
                    "Frecuencia Relativa": frec_relativas,
                    "Probabilidad Teórica": dist_teorica
                })
                st.dataframe(df.style.format({"Frecuencia Relativa": "{:.4f}", "Probabilidad Teórica": "{:.4f}"}), use_container_width=True, hide_index=True)


    # ==========================================
    # EXPERIMENTO 3: BOLAS (URNA)
    # ==========================================
    elif experimento == "Extracción de bolas":
        st.header("🔴🔵 Extracción de bolas de una urna")
        
        c1, c2 = st.columns(2)
        rojas = c1.number_input("Bolas Rojas 🔴", min_value=1, value=5)
        azules = c2.number_input("Bolas Azules 🔵", min_value=1, value=5)
        
        total = rojas + azules
        st.info(f"Total en la urna: {total} bolas.")
        
        extracciones = st.slider("¿Cuántas bolas sacamos por experimento?", 1, total, min(2, total))
        num_experimentos = st.number_input("¿Cuántas veces repetimos el experimento?", min_value=10, value=1000)
        
        reemplazo = st.radio("Método de extracción:", ["Con reemplazamiento (devuelvo la bola)", "Sin reemplazamiento"])
        
        if st.button("Extraer bolas"):
            with st.spinner('Mezclando la urna...'):
                time.sleep(1)
                
                if "Con reemplazamiento" in reemplazo:
                    prob_roja = rojas / total
                    resultados = np.random.binomial(extracciones, prob_roja, size=num_experimentos)
                    # teorica: formula binomial
                    prob_teoricas = [math.comb(extracciones, r) * (prob_roja**r) * ((1-prob_roja)**(extracciones-r)) for r in range(extracciones + 1)]
                else:
                    # hipergeometrica para sin reemplazo
                    resultados = np.random.hypergeometric(ngood=rojas, nbad=azules, nsample=extracciones, size=num_experimentos)
                    # teorica hipergeometrica
                    prob_teoricas = []
                    for r in range(extracciones + 1):
                        if r <= rojas and (extracciones-r) <= azules:
                            p = (math.comb(rojas, r) * math.comb(azules, extracciones-r)) / math.comb(total, extracciones)
                        else:
                            p = 0
                        prob_teoricas.append(p)
                
                frec_absolutas = [np.sum(resultados == i) for i in range(extracciones + 1)]
                frec_relativas = [f / num_experimentos for f in frec_absolutas]
                
                st.success("¡Extracciones terminadas!")
                
                fig, ax = plt.subplots(figsize=(10, 4))
                x = np.arange(extracciones + 1)
                w = 0.4
                
                ax.bar(x - w/2, frec_relativas, w, label="Frecuencia experimental", color="red")
                ax.bar(x + w/2, prob_teoricas, w, label="Prob. Teórica", color="gray")
                
                ax.set_xticks(x)
                ax.set_xlabel("Número de bolas rojas sacadas")
                ax.set_ylabel("Probabilidad")
                
                preparar_grafica(ax)
                ax.legend()
                
                st.pyplot(fig)
                
                # Tabla resumen para las bolas
                st.write("**Tabla comparativa:**")
                df_bolas = pd.DataFrame({
                    "Bolas Rojas Sacadas": x,
                    "Frecuencia Abs": frec_absolutas,
                    "Frecuencia Relativa": frec_relativas,
                    "Probabilidad Teórica": prob_teoricas
                })
                st.dataframe(df_bolas.style.format({"Frecuencia Relativa": "{:.4f}", "Probabilidad Teórica": "{:.4f}"}), use_container_width=True, hide_index=True)
