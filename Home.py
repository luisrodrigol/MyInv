import streamlit as st
from PIL import Image
from streamlit.components.v1 import html
from modules.utility import login_warning,page_setting
from streamlit_login_auth_ui.widgets import __login__



page_setting(
    page_title='Home-MyInv',
    icon='house'
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html= True)

__login__obj = __login__(auth_token = "dk_prod_743TYK5ES04362MPF6FK345A5WR5",
                    company_name = "MyInv",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()

#img1=Image.open('assets/fixed.png')
#st.image(img1)

#if LOGGED_IN == True:
if 'LOGGED_IN' in st.session_state and st.session_state.LOGGED_IN:
   
   def nav_page(page_name, timeout_secs=0.5):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

   
   col1, col2, col3 = st.columns(3)
   
   #st.markdown(st.session_state)
   with col1:
       img3=Image.open('assets/fixed1.png')
       st.image(img3)
   
   st.write('Olá, '+ f'**{username}**')
   st.write('Bem vindo(a) ao **MyInv**...uma aplicação simples para criar e gerenciar inventários de ativos.')

   with col3:
      img2=Image.open('assets/uni7.png')
      st.image(img2)

   with col2:
      if st.button('Ir para Painel de Inventários'):
          nav_page('MyInv_Manager')
    
      
            
    

else:
        login_warning()
                                      