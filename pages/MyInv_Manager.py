import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
from modules.utility import login_warning,page_setting
from streamlit_login_auth_ui.widgets import __login__
import sqlite3

page_setting(
    page_title='MyInv-Manager',
    icon='books'
)

# Create an SQL database connection
conn = sqlite3.connect('myinv.db',timeout=1)
c = conn.cursor()


# Create a table to store inventory information
c.execute('''
    CREATE TABLE IF NOT EXISTS inventarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user TEXT NOT NULL,
        CONSTRAINT "chave" UNIQUE("name","user")        
    )
''')
conn.commit()
conn.close()

__login__obj = __login__(auth_token = "dk_prod_743TYK5ES04362MPF6FK345A5WR5",
                    company_name = "MyInv",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
user= __login__obj.get_username()

#user = username

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html= True)

def main():

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
       
    st.title('📚 Gerenciamento de Inventários')

    st.write('➕ Crie aqui seus inventários')

    with st.form('create'):
        name = st.text_input('Nome:', placeholder='Digite aqui um nome para o inventário')
        if st.form_submit_button('Criar'):
            try:
                if name != '':
                    conn = sqlite3.connect('myinv.db',timeout=1)
                    c = conn.cursor()                    
                    c.execute("INSERT INTO inventarios(name,user) VALUES(?,?)",(name,user))                    
                    conn.commit()
                    conn.close()                    
                    st.success("Inventário criado com sucesso!")                    
                else:
                    st.warning('Informe um nome para o inventário!',icon="⚠️")
            except Exception as e:
                st.warning("Não foi possível cadastrar o inventário",icon="⚠️")
                st.warning("Error: {}".format(e))
                pass
         
    #st.divider()
    st.write('*___________________________________________________________________________________________*')            
    st.write('🖥️ Gerencie aqui seus inventários')

    conn = sqlite3.connect('myinv.db',timeout=1)
    c = conn.cursor()
    c.execute('select name, id from inventarios where user=?',[user])               
    invs = c.fetchall()
    conn.close()
    df = pd.DataFrame(invs)

    def get_new_values_list():
            pass
            #st.markdown(st.session_state['MyInv:'])
            
            
    try:
        inv = st.selectbox('MyInv:',df,on_change=get_new_values_list,key='MyInv:')    
    #st.write(inv)
    except Exception as e:
                    st.warning(
                        "Não há inventários criados!", icon="⚠️")
       
    

    with st.form('manage'):
        # c.execute('select name, id from inventarios where user=?',[user])               
        # invs = c.fetchall()
        # df = pd.DataFrame(invs)

                          

        col1, col2 = st.columns([1,9])
        with col1:
            if st.form_submit_button('Abrir'):
                conn = sqlite3.connect('myinv.db',timeout=1)
                c = conn.cursor()
                sendinv = c.execute('select id, name from inventarios where name=? and user=?',(inv,user)).fetchone()
                st.session_state.invid = sendinv
                conn.close()                
                nav_page('MyInv_Operation')
            
        with col2:     
            if st.form_submit_button('Excluir'):
                try:
                    conn = sqlite3.connect('myinv.db',timeout=1)
                    c = conn.cursor()
                    c.execute('delete from inventarios where name=? and user=?',(inv,user))
                    conn.commit()
                    conn.close()                    
                    st.success('Inventário excluído com sucesso!')
                except Exception as e:
                    st.warning(
                        "Não foi possível excluir o inventário", icon="⚠️")
                    st.warning("Error: {}".format(e))
                    pass


            

    


if __name__ == '__main__':
    # LOGGED_IN key is defined by streamlit_login_auth_ui in the session state.
    if 'LOGGED_IN' in st.session_state and st.session_state.LOGGED_IN:
        main()
    else:
        login_warning()