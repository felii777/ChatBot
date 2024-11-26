import streamlit as st  # type: ignore
from groq import Groq  # type: ignore

st.set_page_config(page_title='Mi primera app en streamlit', page_icon='smile', initial_sidebar_state='collapsed')

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def configurar_page():
    st.sidebar.title('Mi app con IA')
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    
    if elegirModelo == 'llama3-8b-8192':
        st.title('Mi Sesión de llama3-8b-8192')
        st.subheader('llama3-8b-8192')
    elif elegirModelo == 'llama3-70b-8192':
        st.title('Mi Sesión de llama3-70b-8192')
        st.subheader('llama3-70b-8192')
    else:
        st.title('Mi Sesión de mixtral-8x7b-32768')
        st.subheader('mixtral-8x7b-32768')
    
    st.sidebar.write(f'Elejiste el modelo de: {elegirModelo}')
    
    return elegirModelo

def config_user_groq():
    api_key = st.secrets["API_KEY"]
    return Groq(api_key=api_key)

def config_model(cliente, modelo, mensajeDeEntrada):
    response = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )
    return response

def cache():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()

def main():
    modelo = configurar_page()
    clienteUsuario = config_user_groq()
    cache()

    mensaje = st.chat_input("Escribe tu mensaje:")

    if mensaje:
        actualizar_historial("user", mensaje, "😎")

        chat_completo = config_model(clienteUsuario, modelo, mensaje)

        respuesta_completa = ""
        for frase in chat_completo:
            if frase.choices[0].delta.content:
                respuesta_completa += frase.choices[0].delta.content

        actualizar_historial("assistant", respuesta_completa, "😎")

    area_chat()

if __name__ == "__main__":
    main()
