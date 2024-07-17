import streamlit as st
import random
import time

# Configuración de la página
st.set_page_config(page_title="FA FITNESS - Generador de Rutinas", layout="wide")

# Diccionario de ejercicios por grupo muscular con iconos
ejercicios = {
    "💪 Brazos": ["Curl de bíceps", "Extensiones de tríceps", "Pushups"],
    "🦵 Piernas": ["Sentadillas", "Estocadas", "Peso muerto"],
    "🏋️ Abdominales": ["Crunches", "Plancha", "Russian twists"],
    "🏋️ Hombros": ["Press militar", "Elevaciones laterales", "Face pulls"],
    "🏃 Aeróbico": ["Saltar la cuerda", "Burpees", "Mountain climbers"]
}

# Distribución de ejercicios según la priorización
distribucion_ejercicios = {
    "Tren superior": {"💪 Brazos": 3, "🏋️ Hombros": 2, "🏋️ Abdominales": 1, "🦵 Piernas": 1, "🏃 Aeróbico": 1},
    "Zona media": {"🏋️ Abdominales": 3, "💪 Brazos": 2, "🦵 Piernas": 1, "🏋️ Hombros": 1, "🏃 Aeróbico": 1},
    "Tren inferior": {"🦵 Piernas": 3, "🏋️ Abdominales": 2, "💪 Brazos": 1, "🏋️ Hombros": 1, "🏃 Aeróbico": 1},
    "Aeróbico": {"🏃 Aeróbico": 3, "🦵 Piernas": 2, "💪 Brazos": 1, "🏋️ Abdominales": 1, "🏋️ Hombros": 1}
}

def generar_rutina(prioridad, duracion):
    rutina = []
    for grupo, cantidad in distribucion_ejercicios[prioridad].items():
        ejercicios_grupo = random.sample(ejercicios[grupo], cantidad)
        for ejercicio in ejercicios_grupo:
            if duracion == "Ambos aleatorios":
                tiempo = random.choice([30, 40])
            else:
                tiempo = int(duracion.split()[0])
            rutina.append((grupo, ejercicio, tiempo))
    random.shuffle(rutina)
    return rutina

def mostrar_rutina(rutina):
    st.title("🏋️ FA FITNESS - Tu Rutina Personalizada")
    for grupo, ejercicio, duracion in rutina:
        st.write(f"{grupo} - {ejercicio}: {duracion} segundos")

def temporizador(rutina):
    st.title("🏋️ FA FITNESS - Temporizador de Rutina")
    
    if 'ejercicio_actual' not in st.session_state:
        st.session_state.ejercicio_actual = 0
        st.session_state.tiempo_restante = rutina[0][2]
        st.session_state.en_descanso = False
    
    grupo, ejercicio, duracion = rutina[st.session_state.ejercicio_actual]
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"<h1 style='text-align: center;'>{grupo}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{ejercicio}</h2>", unsafe_allow_html=True)
        
        progress = st.progress(0)
        tiempo_texto = st.empty()
        
        if st.button("Pausar/Reanudar", key="pausar_reanudar"):
            st.session_state.timer_running = not st.session_state.timer_running
    
    if st.session_state.timer_running:
        if st.session_state.en_descanso:
            total_tiempo = 10
        else:
            total_tiempo = duracion
        
        progress.progress(1 - st.session_state.tiempo_restante / total_tiempo)
        tiempo_texto.markdown(f"<h3 style='text-align: center;'>{st.session_state.tiempo_restante} segundos</h3>", unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.tiempo_restante -= 1
        
        if st.session_state.tiempo_restante < 0:
            if st.session_state.en_descanso:
                st.session_state.en_descanso = False
                st.session_state.ejercicio_actual += 1
                if st.session_state.ejercicio_actual < len(rutina):
                    st.session_state.tiempo_restante = rutina[st.session_state.ejercicio_actual][2]
                else:
                    st.success("¡Felicidades! Has completado tu rutina.")
                    if st.button("Volver al inicio", key="volver_inicio"):
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.experimental_rerun()
                    return
            elif st.session_state.ejercicio_actual < len(rutina) - 1:
                st.session_state.en_descanso = True
                st.session_state.tiempo_restante = 10
            else:
                st.success("¡Felicidades! Has completado tu rutina.")
                if st.button("Volver al inicio", key="volver_inicio"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.experimental_rerun()
                return
        
        st.experimental_rerun()

def main():
    if 'rutina' not in st.session_state:
        st.title("🏋️ FA FITNESS - Generador de Rutinas")
        
        prioridad = st.selectbox(
            "Selecciona la prioridad de tu rutina:",
            ["Tren superior", "Zona media", "Tren inferior", "Aeróbico"]
        )
        
        duracion = st.selectbox(
            "Selecciona la duración de los ejercicios:",
            ["30 segundos", "40 segundos", "Ambos aleatorios"]
        )
        
        if st.button("Generar Rutina", key="generar_rutina"):
            st.session_state.rutina = generar_rutina(prioridad, duracion)
            st.session_state.prioridad = prioridad
            st.session_state.duracion = duracion
            st.experimental_rerun()
    
    elif 'timer_running' not in st.session_state or not st.session_state.timer_running:
        mostrar_rutina(st.session_state.rutina)
        
        col1, col2 = st.columns(2)
        if col1.button("🔄 Refresh Rutina", key="refresh_rutina"):
            st.session_state.rutina = generar_rutina(st.session_state.prioridad, st.session_state.duracion)
            st.experimental_rerun()
        
        if col2.button("Iniciar Temporizador", key="iniciar_temporizador_main"):
            st.session_state.timer_running = True
            st.experimental_rerun()
    
    else:
        temporizador(st.session_state.rutina)

if __name__ == "__main__":
    main()