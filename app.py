import streamlit as st
from PIL import Image
from modules.utility import login_warning
from streamlit_login_auth_ui.widgets import __login__

__login__obj = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()

img1=Image.open('assets/fixed.png')
st.image(img1)

#if LOGGED_IN == True:
if 'LOGGED_IN' in st.session_state and st.session_state.LOGGED_IN:

   
   #st.markdown(st.session_state)
   st.write('Olá, '+username)
   st.write('Bem vindo(a) ao **MyInv**...uma aplicação simples para criar e gerenciar inventários de ativos.')
   img2=Image.open('assets/uni7.png')
   st.image(img2)

else:
        login_warning()
                                      
