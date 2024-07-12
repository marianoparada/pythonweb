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
        options=["Inicio","General", "Liga", "Equipo", "Jugador"],  # Opciones del menú
        icons=["house","newspaper", "trophy", "people", "person"],  # Iconos de las opciones
        menu_icon="list",  # Icono del menú
        default_index=0,  # Índice de la opción predeterminada
    )

# Funciones para cada opción

def home():
    # Título del dashboard
    st.title('📊 Estadísticas de fobal ...')
    st.write('Extraído con Web Scraping de: https://salarysport.com/football/')
    st.caption("Realizado por Lic. Mariano Parada - Data Scientists - mariano.parada@gmail.com - 2024")
    
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

    # Usamos st.empty() para crear contenedores que podemos actualizar
    liga_container = st.empty()
    edad_container = st.empty()
    metricas_container = st.empty()
    top10_container = st.empty()
    top20_container = st.empty()
    club_container = st.empty()
    comparativa_container = st.empty()

    liga_seleccionada = liga_container.selectbox('Selecciona una Liga', df['liga'].unique())
    df_liga = df[df['liga'] == liga_seleccionada]

    # Distribución de edades en la liga seleccionada
    fig_edad_liga = px.histogram(df_liga, x='edad', nbins=20, labels={'edad': 'Edad'}, title=f'Distribución de Edades en {liga_seleccionada}')
    edad_container.plotly_chart(fig_edad_liga)

    # Métricas de la liga
    col1, col2 = metricas_container.columns(2)
    col1.metric(f'Salario Promedio Anual en {liga_seleccionada}', f'${df_liga["salario_anual"].mean():,.2f}')
    col2.metric(f'Valor Total de Mercado en {liga_seleccionada}', f'${df_liga["salario_anual"].sum():,.2f}')

    # 1. Top 10 jugadores mejor pagados de la liga
    top10_container.subheader(f'Top 10 Jugadores Mejor Pagados de {liga_seleccionada}')
    top_10_jugadores = df_liga.nlargest(10, 'salario_anual')[['jugador', 'club', 'salario_anual']]
    top_10_jugadores['salario_anual'] = top_10_jugadores['salario_anual'].apply(lambda x: f'${x:,.0f}')
    top10_container.table(top_10_jugadores)

    # 2. Promedio de sueldo por equipo de los 20 jugadores mejor pagados de cada plantel
    top20_container.subheader(f'Promedio de Sueldo de Top 20 Jugadores por Equipo en {liga_seleccionada}')
    
    def top_20_avg(group):
        return group.nlargest(20, 'salario_anual')['salario_anual'].mean()

    promedio_top_20 = df_liga.groupby('club').apply(top_20_avg).sort_values(ascending=False)
    fig_promedio_top_20 = px.bar(promedio_top_20, x=promedio_top_20.index, y=promedio_top_20.values,
                                 labels={'x': 'Club', 'y': 'Promedio Salarial Top 20'},
                                 title=f'Promedio Salarial de Top 20 Jugadores por Club en {liga_seleccionada}')
    top20_container.plotly_chart(fig_promedio_top_20)

    # Análisis por Club
    club_container.header('Análisis por Club')
    club_seleccionado = club_container.selectbox('Selecciona un Club', df_liga['club'].unique())
    df_club = df_liga[df_liga['club'] == club_seleccionado]

    # Distribución de posiciones en el club seleccionado
    fig_posicion_club = px.bar(df_club['posición'].value_counts(), labels={'index': 'Posición', 'value': 'Número de Jugadores'}, title=f'Distribución de Posiciones en {club_seleccionado}')
    club_container.plotly_chart(fig_posicion_club)

    # Métricas del club
    col1, col2 = club_container.columns(2)
    col1.metric(f'Salario Promedio Anual en {club_seleccionado}', f'${df_club["salario_anual"].mean():,.2f}')
    col2.metric(f'Valor Total de Mercado en {club_seleccionado}', f'${df_club["salario_anual"].sum():,.2f}')

    # Comparativa entre Ligas/Clubs
    comparativa_container.header('Comparativa entre Ligas/Clubs')

    # Comparativa de salario promedio entre ligas
    salario_promedio_ligas = df.groupby('liga')['salario_anual'].mean().sort_values(ascending=False)
    fig_salario_ligas = px.bar(salario_promedio_ligas, x=salario_promedio_ligas.index, y=salario_promedio_ligas.values, labels={'x': 'Liga', 'y': 'Salario Promedio Anual'}, title='Comparativa de Salario Promedio entre Ligas')
    comparativa_container.plotly_chart(fig_salario_ligas)

    # Comparativa de valor total de mercado entre clubs
    valor_total_clubs = df.groupby('club')['salario_anual'].sum().sort_values(ascending=False)
    fig_valor_clubs = px.bar(valor_total_clubs, x=valor_total_clubs.index, y=valor_total_clubs.values, labels={'x': 'Club', 'y': 'Valor Total de Mercado (USD)'}, title='Comparativa de Valor Total de Mercado entre Clubs')
    comparativa_container.plotly_chart(fig_valor_clubs)
    
    
    

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





# Mostrar el contenido basado en la selección del menú
if selected == "Inicio":
    home()

if selected == "Datos Generales":
    mostrar_datos_generales()
elif selected == "Liga":
    mostrar_datos_liga()
elif selected == "Equipo":
    mostrar_datos_equipo()
elif selected == "Jugador":
    mostrar_datos_jugador()