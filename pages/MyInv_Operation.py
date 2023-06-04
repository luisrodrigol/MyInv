import streamlit as st
import datetime as dt
import pandas as pd
from modules.utility import login_warning,page_setting
from streamlit_login_auth_ui.widgets import __login__
from streamlit_cookies_manager import EncryptedCookieManager
import sqlite3
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report
import locale
import altair as alt







page_setting(
    page_title='MyInv-Operation',
    icon='bar_chart',
    layout='wide'
    
)



# Create an SQL database connection
conn = sqlite3.connect('myinv.db',timeout=1)
c = conn.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS inventario (
        inv_id INTEGER NOT NULL,
        ativo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        categoria TEXT NOT NULL,
        local TEXT NOT NULL,
        ambiente TEXT,
        valor REAL not null,
        data_aquisicao DATE not null

    )
''')
conn.commit()


__login__obj = __login__(auth_token = "dk_prod_743TYK5ES04362MPF6FK345A5WR5",
                    company_name = "MyInv",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
user= __login__obj.get_username()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html= True)


def main():
    
    if 'invid' in st.session_state:
        pass

        def atualizadb():
           
         newdb = c.execute('SELECT ativo_id as "ATIVO", descricao as "DESCRICAO",categoria as "CATEGORIA",local as "LOCAL",ambiente as "AMBIENTE",valor as "VALOR",data_aquisicao as "DATA DA AQUISICÃO" from inventario where inv_id=?',[st.session_state.invid[0]]).fetchall()        
         
         return newdb

        

        def buscar(ativo,descricao,categoria,ambiente,valor,datade,datapara):
            format = '%Y-%m-%d'
            
            #blocoformat = '%Y/%m/%d'
            if ativo != "": ativob = ativo 
            else: ativob = None
            if descricao != "": descricaob = descricao 
            else: descricaob = None
            if categoria != "": categoriab = categoria 
            else: categoriab = None
            if ambiente != "": ambienteb = ambiente 
            else: ambienteb = None
            if valor != "": valorb = valor 
            else: valorb = None
            if datade != "":
               
               try:
                
                res = bool(dt.datetime.strptime(str(datade),format))                

                if res:               
                    datadeb = dt.datetime.strptime(str(datade),format)
                    datadeb = datadeb - dt.timedelta(1)
                else:
                    datadeb = dt.datetime.strptime(str(datade),'%d/%m/%Y').date()                                       
                    datadeb = datadeb - dt.timedelta(1)
                
                   
               except Exception as e:
                  st.warning("Formato de data deve ser YYYY-MM-DD", icon="⚠️")
                  st.warning("Error: {}".format(e))
                  
            else: datadeb = None
            if datapara != "": 
               dataparab = dt.datetime.strptime(str(datapara),format)
               #dataparab = dataparab + dt.timedelta(1) 
            else: dataparab = None

            
            busca=c.execute('SELECT ativo_id as "ATIVO", descricao as "DESCRICAO",categoria as "CATEGORIA",local as "LOCAL",ambiente as "AMBIENTE",valor as "VALOR",data_aquisicao as "DATA DA AQUISICÃO" from inventario where inv_id=?1 and ativo_id = coalesce(?2,ativo_id) and descricao = coalesce(?3,descricao) and categoria = coalesce(?4,categoria) and ambiente = coalesce(?5,ambiente) and valor = coalesce(?6,valor) and data_aquisicao >= coalesce(?7,data_aquisicao) and data_aquisicao <= coalesce(?8,data_aquisicao)',(st.session_state.invid[0],ativob,descricaob,categoriab,ambienteb,valorb,datadeb,dataparab)).fetchall()
            
            return busca

            
        
        st.title('🖥️📊 Operação e Análise')
        st.divider()
        
        
            
        
        invop = c.execute('select name,id from inventarios where id=?',[st.session_state.invid[0]]).fetchone()
        
        #tt = c.execute("select sum(valor) from inventario where inv_id=?",[st.session_state.invid[0]]).fetchone()
        st.subheader('🖥️ Myinv: '+ str(invop[0]).capitalize())
    try:   
        
        
        #exibir = c.execute('SELECT ativo_id as "ATIVO", descricao as "DESCRICAO",categoria as "CATEGORIA",local as "LOCAL",ambiente as "AMBIENTE",valor as "VALOR",data_aquisicao as "DATA DA AQUISICÃO" from inventario where inv_id=?',[st.session_state.invid[0]]).fetchall()        
        exibir = atualizadb()
        
        
        col1,col2 = st.columns([1,1.1])
        

        with col1:
            with st.form('oper'):
                 col3,col4,col5,col6 = st.columns([0.6,0.07,0.3,0.3])
                

                 with col3:                 
                  st.markdown('####')
                  ativo      =   st.text_input('Ativo:')
                  descricao  =   st.text_input('Descrição')
                  categoria	=	st.text_input('Categoria:') 
                  ambiente	=	st.text_input('Ambiente:')                 

                 with col5:
                   st.write('')
                   valor	    =	st.text_input('Valor:')
                   datade	    =	st.text_input('DT de Aqs.-DE:')
                   datapara	    =	st.text_input('DT de Aqs.-ATÉ:')

                   if st.form_submit_button('Buscar'):
                      try:
                         
                         exibir=buscar(ativo,descricao,categoria,ambiente,valor,datade,datapara)
                         
                         
                         
                         
                      except Exception as e:
                           st.warning(
                             "Por gentileza, passe valores válidos!", icon="⚠️")
                           st.warning("Error: {}".format(e))
                           pass
                                             
                   if st.form_submit_button('Incluir'):
                      if descricao == '' or categoria == '' or ambiente == '' or valor == '' or datade == '':
                       st.warning("Insira no mínimo os valores de: descricao, categoria, valor e data de aquisição", icon="⚠️")
                      else:
                        try:                            
                                
                            c.execute("INSERT INTO inventario (inv_id,descricao,categoria,local,ambiente,valor,data_aquisicao) values(?,?,?,?,?,?,?)",(st.session_state.invid[0],descricao,categoria,invop[1],ambiente,valor,datade)).connection.commit()
                            st.success('Ativo adicionado com sucesso!')

                        except Exception as e:
                            st.warning("A inclusão não pode ser realizada, insira valores válidos", icon="⚠️")
                            st.warning("Error: {}".format(e))
                            pass
                        exibir = atualizadb()
                   
                   
                 with col6:
                   def space():
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                    st.markdown('####')
                   
                   space()
                   if st.form_submit_button('Alterar'):
                      if descricao == '' or ativo == '':
                          st.warning("Apenas a descrição pode ser alterada, informe-a junto com o ativo!", icon="⚠️")
                          
                      else:
                          try:
                              c.execute("UPDATE inventario set descricao = ? where inv_id = ? and ativo_id = ?",(descricao,st.session_state.invid[0],ativo)).connection.commit()
                              st.success("Alteração realizada!")
                          except Exception as e:
                            st.warning("A alteração não pode ser realizada!", icon="⚠️")
                            st.warning("Error: {}".format(e))
                            pass    
                      exibir = atualizadb()
                   
                   if st.form_submit_button('Baixar'):
                      
                     valida = c.execute('select inv_id from inventario where inv_id= ? and ativo_id= ?',(st.session_state.invid[0],ativo)).fetchone()
                     
                     if valida == None:st.warning("Error: A baixa é a nível de ativo, informe um número de ativo válido!", icon="⚠️")

                     elif str(valida[0]) == str(st.session_state.invid[0]):
                     #st.write(valida[0])
                     
                        try:      
                                c.execute("DELETE FROM inventario where ativo_id = ?",[ativo]).connection.commit()                               
                                st.success("Ativo baixado com sucesso!")

                        except Exception as e:
                                st.warning("Error: A baixa é a nível de ativo, informe um número de ativo válido!", icon="⚠️")
                                pass
                     
                     exibir = atualizadb()
                   
                   
                   
                
                    

            
        with col2:
            #st.table(exibir)
            df = pd.DataFrame(exibir,columns=[col[0] for col in c.description])            
            st.dataframe(df.set_index(df.columns[0]))
    
        #============================seção de Dashboards==============================================================================
        st.divider()
        st.subheader('📊Dashboards')

        col1, col2, col3 = st.columns(3)
        #try:
            tt = sum(row[5] for row in exibir)
            
            top=c.execute('SELECT categoria, sum(valor) from inventario where inv_id =? GROUP by categoria order by sum(valor) desc',[st.session_state.invid[0]]).fetchone()
            

            ea=str(dt.date.today().strftime("%Y"))
            aa=str((dt.date.today()- dt.timedelta(days=365)).strftime("%Y"))
            
            
            
            ttea=c.execute('SELECT sum(valor) from inventario where inv_id=?1 and strftime("%Y", date(data_aquisicao)) = ?2',(st.session_state.invid[0],ea)).fetchone()
            
            
            
            ttaa=c.execute('SELECT sum(valor) from inventario where inv_id=?1 and strftime("%Y", date(data_aquisicao)) = ?2',(st.session_state.invid[0],aa)).fetchone()
            
            vscard=ttea[0]-ttaa[0]
            
            
            locale.setlocale( locale.LC_ALL, '' )
            col1.metric(label="**Valor Total**", value=locale.currency(tt,grouping=True ))
            col2.metric(label=f"**{str(ea)} vs AA**", value=locale.currency(ttea[0],grouping=True ), delta=vscard)
            col3.metric(label=f"**Top Categoria: {str(top[0])}**", value=locale.currency(top[1],grouping=True),delta='KPI Estático')
            style_metric_cards()
            st.divider()

            col7, col8,col9 = st.columns([1,0.3,1.1])
            with col7:                
                 with chart_container(df):
                     st.write('**Valor por Categ.**')
                     st.bar_chart(data=df,x='CATEGORIA',y='VALOR')

                 with chart_container(df):
                    st.write('**Valor por Ambiente**')
                    bars = alt.Chart(df).mark_bar().encode(
                    x='VALOR:Q',
                    y="AMBIENTE:O"
                        )
                    
                    text = bars.mark_text(
                    align='left',
                    baseline='middle',
                    dx=3  # Nudges text to right so it doesn't appear on top of the bar
                        ).encode(
                    text='VALOR:Q'
                        )
                    
                    chart = (bars + text)

                    tab1, tab2 = st.tabs(["Tema Azul", "Tema Azul Escuro"])

                    with tab1:
                        st.altair_chart(chart, theme="streamlit", use_container_width=True)
                    with tab2:
                        st.altair_chart(chart, theme=None, use_container_width=True)
                    
            
            with col9:             

                with chart_container(df):
                    st.write('**Share de Categoria**')
                    base = alt.Chart(df).encode(
                    theta=alt.Theta("VALOR:Q", stack=True),
                    radius=alt.Radius("CATEGORIA", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
                    color="CATEGORIA:N",
                    )

                    c1 = base.mark_arc(innerRadius=20, stroke="#fff")

                    c2 = base.mark_text(radiusOffset=10).encode(text="VALOR:Q")

                    chart = c1 + c2

                    tab1, tab2 = st.tabs(["Tema Padrão", "Tema Alternativo"])

                    with tab1:
                        st.altair_chart(chart, theme="streamlit", use_container_width=True)
                    with tab2:
                        st.altair_chart(chart, theme=None, use_container_width=True)

                with chart_container(df):
                    st.write('**Mix de Ambientes**')                
                    fig_category_percent=alt.Chart(df).mark_arc().encode(
                    theta=alt.Theta(field="VALOR", type="quantitative"),
                    color=alt.Color(field="AMBIENTE", type="nominal"))
                    st.altair_chart(fig_category_percent)

            

            st.divider()
            st.subheader('📈Estatísticas')

            pr = df.profile_report()
            st_profile_report(pr)
            
        #except Exception as e:
                st.warning("Inventário vazio!", icon="⚠️")
                pass
        


    except Exception as e:
             st.warning(
                     "Por gentileza, volte a página de gerenciamento e escolha um inventário!", icon="⚠️")
             #st.warning("Error: {}".format(e))
             pass







if __name__ == '__main__':
    # LOGGED_IN key is defined by streamlit_login_auth_ui in the session state.
    if 'LOGGED_IN' in st.session_state and st.session_state.LOGGED_IN:
        main()
    else:
        login_warning()
