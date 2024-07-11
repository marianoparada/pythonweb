import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Estadísticas de fóbal ...",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': "Esta es una aplicación para el análisis de una encuesta sobre consumo de vinos."
    }
)

with st.sidebar:
    selected = option_menu(
        menu_title="Menu",  # Opcional
        options=["Datos Generales", "Liga", "Equipo", "Jugador"],  # Opciones del menú
        icons=["house", "trophy", "people", "person"],  # Iconos de las opciones
        menu_icon="cast",  # Icono del menú
        default_index=0,  # Índice de la opción predeterminada
    )

# Funciones para cada opción
def mostrar_datos_generales():
    # Crear el encabezado
    st.header('📊 Información General - Estadísticas')

    # Métricas generales
    num_ligas = df['liga'].nunique()
    num_clubs = df['club'].nunique()
    num_jugadores = df['jugador'].nunique()

    # Crear columnas para mostrar las métricas horizontalmente
    col1, col2, col3 = st.columns(3)

    # Mostrar las métricas con emojis
    with col1:
        st.metric('🏆 Ligas', num_ligas)

    with col2:
        st.metric('⚽ Clubs', num_clubs)

    with col3:
        st.metric('🧑‍🤝‍🧑 Jugadores', num_jugadores)
    
    # Distribución de jugadores por liga
    liga_counts = df['liga'].value_counts()
    fig_liga = px.bar(liga_counts, x=liga_counts.index, y=liga_counts.values, labels={'x': 'Liga', 'y': 'Número de Jugadores'}, title='Distribución de Jugadores por Liga')
    st.plotly_chart(fig_liga)

    # Distribución de jugadores por nacionalidad
    nacionalidad_counts = df['nacionalidad'].value_counts()
    fig_nacionalidad = px.bar(nacionalidad_counts, x=nacionalidad_counts.index, y=nacionalidad_counts.values, labels={'x': 'Nacionalidad', 'y': 'Número de Jugadores'}, title='Distribución de Jugadores por Nacionalidad')
    st.plotly_chart(fig_nacionalidad)

def mostrar_datos_liga():
    # Análisis por Liga
    st.header(' 🏆 Información de las ligas')

    liga_seleccionada = st.selectbox('Selecciona una Liga', df['liga'].unique())
    df_liga = df[df['liga'] == liga_seleccionada]

    # Distribución de edades en la liga seleccionada
    fig_edad_liga = px.histogram(df_liga, x='edad', nbins=20, labels={'edad': 'Edad'}, title=f'Distribución de Edades en {liga_seleccionada}')
    st.plotly_chart(fig_edad_liga)

    # Promedio de salario anual en la liga seleccionada
    salario_promedio_liga = df_liga['salario_anual'].mean()
    st.metric(f'Salario Promedio Anual en {liga_seleccionada}', f'{salario_promedio_liga:.2f}')

    # Valor total de mercado en la liga seleccionada
    valor_total_liga = df_liga['salario_anual'].sum()
    st.metric(f'Valor Total de Mercado en {liga_seleccionada}', f'{valor_total_liga:.2f} USD')

    # Análisis por Club
    st.header('Análisis por Club')

    club_seleccionado = st.selectbox('Selecciona un Club', df['club'].unique())
    df_club = df[df['club'] == club_seleccionado]

    # Distribución de posiciones en el club seleccionado
    fig_posicion_club = px.bar(df_club['posición'].value_counts(), labels={'index': 'Posición', 'value': 'Número de Jugadores'}, title=f'Distribución de Posiciones en {club_seleccionado}')
    st.plotly_chart(fig_posicion_club)

    # Promedio de salario anual en el club seleccionado
    salario_promedio_club = df_club['salario_anual'].mean()
    st.metric(f'Salario Promedio Anual en {club_seleccionado}', f'{salario_promedio_club:.2f}')

    # Valor total de mercado en el club seleccionado
    valor_total_club = df_club['salario_anual'].sum()
    st.metric(f'Valor Total de Mercado en {club_seleccionado}', f'{valor_total_club:.2f} USD')

    # Comparativa entre Ligas/Clubs
    st.header('Comparativa entre Ligas/Clubs')

    # Comparativa de salario promedio entre ligas
    salario_promedio_ligas = df.groupby('liga')['salario_anual'].mean().sort_values(ascending=False)
    fig_salario_ligas = px.bar(salario_promedio_ligas, x=salario_promedio_ligas.index, y=salario_promedio_ligas.values, labels={'x': 'Liga', 'y': 'Salario Promedio Anual'}, title='Comparativa de Salario Promedio entre Ligas')
    st.plotly_chart(fig_salario_ligas)

    # Comparativa de valor total de mercado entre clubs
    valor_total_clubs = df.groupby('club')['salario_anual'].sum().sort_values(ascending=False)
    fig_valor_clubs = px.bar(valor_total_clubs, x=valor_total_clubs.index, y=valor_total_clubs.values, labels={'x': 'Club', 'y': 'Valor Total de Mercado (USD)'}, title='Comparativa de Valor Total de Mercado entre Clubs')
    st.plotly_chart(fig_valor_clubs)
    
    
    

def mostrar_datos_equipo():
    st.title("⚽ Información de un equipo")
    # Nuevo selector de liga y equipo
    st.header('🏆 Selector de Liga y Equipo')

    # Selector de liga
    liga_seleccionada = st.selectbox(
        '🌍 Selecciona una Liga',
        options=['Todas'] + sorted(df['liga'].unique().tolist())
    )

    # Filtrar equipos basados en la liga seleccionada
    if liga_seleccionada == 'Todas':
        equipos = sorted(df['club'].unique())
    else:
        equipos = sorted(df[df['liga'] == liga_seleccionada]['club'].unique())

    # Selector de equipo
    equipo_seleccionado = st.selectbox(
        '⚽ Selecciona un Equipo',
        options=equipos
    )

    # Mostrar datos de la plantilla del equipo seleccionado
    if equipo_seleccionado:
        st.subheader(f'📋 Plantilla de {equipo_seleccionado}')
        
        plantilla = df[df['club'] == equipo_seleccionado].sort_values('salario_anual', ascending=False)
        
        # Crear una tabla formateada
        tabla_plantilla = plantilla[['jugador', 'edad', 'nacionalidad', 'salario_anual']].copy()
        tabla_plantilla['salario_anual'] = tabla_plantilla['salario_anual'].apply(lambda x: f"${x:,.0f}")
        tabla_plantilla.columns = ['🧑 Jugador', '🎂 Edad', '🏴 Nacionalidad', '💰 Salario Anual(usd)']
        
        st.table(tabla_plantilla)

        # Calcular y mostrar estadísticas del equipo
        salario_total = plantilla['salario_anual'].sum()
        salario_promedio = plantilla['salario_anual'].mean()
        jugador_mejor_pagado = plantilla.iloc[0]['jugador']
        jugador_peor_pagado = plantilla.iloc[-1]['jugador']

        st.subheader(f'📊 Estadísticas de: {equipo_seleccionado}')
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💼 Salario Total del Equipo", f"${salario_total:,.0f}")
            st.metric("🏅 Jugador Mejor Pagado", jugador_mejor_pagado)
        with col2:
            st.metric("📈 Salario Promedio", f"${salario_promedio:,.0f}")
            st.metric("🏐 Jugador Peor Pagado", jugador_peor_pagado)
    
    
    

def mostrar_datos_jugador():
    # Análisis Individual
    st.header('🏃 Análisis Individual')

    # Buscador de jugadores
    jugador_seleccionado = st.selectbox(
        'Busca un Jugador', 
        df['jugador'].unique()
    )

    df_jugador = df[df['jugador'] == jugador_seleccionado]

    if not df_jugador.empty:
        st.write(df_jugador[['jugador', 'edad', 'nacionalidad', 'liga', 'club', 'salario_anual']])
        
        # Datos del jugador
        sueldo_jugador = df_jugador['salario_anual'].values[0]
        club_jugador = df_jugador['club'].values[0]
        liga_jugador = df_jugador['liga'].values[0]

        # Promedios y máximos
        promedio_mundial = df['salario_anual'].mean()
        maximo_mundial = df['salario_anual'].max()
        
        promedio_liga = df[df['liga'] == liga_jugador]['salario_anual'].mean()
        maximo_liga = df[df['liga'] == liga_jugador]['salario_anual'].max()
        
        promedio_club = df[df['club'] == club_jugador]['salario_anual'].mean()
        maximo_club = df[df['club'] == club_jugador]['salario_anual'].max()

        # Posición del sueldo del jugador
        posicion_mundial = df['salario_anual'].rank(ascending=False).loc[df_jugador.index].values[0]
        posicion_liga = df[df['liga'] == liga_jugador]['salario_anual'].rank(ascending=False).loc[df_jugador.index].values[0]
        posicion_club = df[df['club'] == club_jugador]['salario_anual'].rank(ascending=False).loc[df_jugador.index].values[0]

    # Posición del sueldo
        # Análisis Individual
        st.header(f'💵 Posición del sueldo de {jugador_seleccionado}')
        st.write(f'Mundo 🌍 #', int(posicion_mundial), ' | Liga 🏆 #', int(posicion_liga), ' | Club 🏟️ #', int(posicion_club))
        url='https://www.youtube.com/results?search_query=Soccer%2B'+jugador_seleccionado+'&sp=CAA%253D'
        url=url.replace(" ", "%2B")
        # Mostrar el enlace en Streamlit
        st.markdown(f"🎥 >>  [Ver videos más vistos sobre {jugador_seleccionado} en YouTube]({url})")

        # Permitir al usuario ingresar la URL del video más visto manualmente

        # Gráfico comparativo
        fig_comparativa = go.Figure()
        
        fig_comparativa.add_trace(go.Bar(
            x=['Promedio Mundial', 'Promedio Mundial'],
            y=[promedio_mundial],
            name='Mundial',
            marker_color='blue'
        ))
        
        fig_comparativa.add_trace(go.Bar(
            x=['Promedio Liga', 'Promedio Liga'],
            y=[promedio_liga],
            name=liga_jugador,
            marker_color='green'
        ))
        
        fig_comparativa.add_trace(go.Bar(
            x=['Promedio Club', 'Promedio Club'],
            y=[promedio_club],
            name=club_jugador,
            marker_color='red'
        ))

        fig_comparativa.add_trace(go.Bar(
            x=['Sueldo Jugador', 'Sueldo Jugador'],
            y=[sueldo_jugador],
            name=jugador_seleccionado,
            marker_color='orange'
        ))

        fig_comparativa.update_layout(
            title=f'Comparativa de Sueldo de {jugador_seleccionado}',
            barmode='group'
        )
        
        st.plotly_chart(fig_comparativa)
    else:
        st.write('Jugador no encontrado.')





# Cargar los datos
df = pd.read_excel('jugadores.xlsx')
df = df.drop_duplicates()
df = df[df['liga'] != 'J1-League']
df = df[df['liga'] != 'j1-league']
df = df[df['liga'] != 'national-league']
df = df[df['liga'] != 'indian-super-league']
df = df[df['liga'] != 'thai-league']
df = df[df['liga'] != 'i-league']
df = df[df['liga'] != 'scottish-championship']
df = df[df['liga'] != 'league-two']
df = df[df['liga'] != 'ekstraklasa']
df = df[df['liga'] != 'other']
df = df[df['liga'] != 'ligue-2']

# Filtramos los salarios que cobren menos de 2.000 USD por mes
df = df[df['salario_anual'] >= 24000]

# Título del dashboard
st.title('📊 Estadísticas de fobal ...')
st.write('Extraído con Web Scraping de: https://salarysport.com/football/')
st.caption("Realizado por Lic. Mariano Parada - Data Scientists - mariano.parada@gmail.com - 2024")



# Mostrar el contenido basado en la selección del menú
if selected == "Datos Generales":
    mostrar_datos_generales()
elif selected == "Liga":
    mostrar_datos_liga()
elif selected == "Equipo":
    mostrar_datos_equipo()
elif selected == "Jugador":
    mostrar_datos_jugador()