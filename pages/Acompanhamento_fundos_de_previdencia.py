#---------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------Importing libraries----------------------------------------------------------# 

import pandas as pd
import dash_mantine_components as dmc
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html
from dash import Dash, Input, Output, callback_context as ctx, dash_table, State, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import json
from dash_bootstrap_templates import load_figure_template
import datetime
import base64
import dash


#--------------------------------------------------------------------------------------------------------------------------------#



#----------------------------------------Importing components and data----------------------------------------------------------#



#Importing dataframes, altering format style, importing images and templates


df = pd.DataFrame(pd.read_excel(r'C:\Users\Gustavo.vieira\Desktop\python\estudos_dash\watchlist_project\data\acompanhamento_prev.xlsx'))

dff= pd.DataFrame(df[['Nome','Classificação CVM','retorno no mês','retorno no ano', 'retorno 12 meses','retorno 24 meses', 'retorno 36 meses', 'retorno desde o inicio', 'volatilidade 12 meses', 'Indicator Name']]).copy()
start_df = pd.DataFrame(dff[['Nome','Classificação CVM','retorno no mês','retorno no ano', 'retorno 12 meses']])

#Formating columns of dataframe.ALWAYS use dff or derivatives, never df itself
valores = ['retorno no mês','retorno no ano', 'retorno 12 meses','retorno 24 meses', 'retorno 36 meses', 'retorno desde o inicio', 'volatilidade 12 meses']
columns_teste = ['retorno no mês','retorno no ano', 'retorno 12 meses']

for i in valores:
    dff[i] = df[i].fillna(0).astype(float).map(lambda n: '{:.2%}'.format(n))


#variable used to insert dash.table.Datatable
db_filtered = pd.DataFrame(dff)
#db_filtered = db_filtered.loc[:,['Nome','tipo']]


#logo of BRA
image_filename = r'C:\Users\Gustavo.vieira\Desktop\python\estudos_dash\watchlist_project\data\logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode()



#Design of elements inside dashboard
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template('SOLAR')






#---------------------------------------------------------------------------------------------------------------------------------------#

#  1. FUNCTIONS CONSTRUCTION

        # 1.1 - table_creation
            

#---------------------------------------------------------------------------------------------------------------------------------------#
dash.register_page(__name__)

#------------------------------------------------------- 1.1 ---------------------------------------------------------------------------#

def table_creation(dff):
    #db_as_list = db_filtered.columns.to_list()
    # print(db_as_list)
    table = dash_table.DataTable(
        data=[{

        }],
        columns=[{"name": i,
                  "id": i
                  } for i in dff],  # <------------ setting columns of datatable
        editable=False,  # <------------ setting preferences if is or not editable
        filter_action="native",  # <------------ Filters in columns
        sort_action="native",  # <------------  # <------------
        column_selectable="single",  # <------------ Selectable only one column
        row_selectable=False,  # <------------  dont let select just a row
        selected_columns=[],  # <------------ no column is selected previously
        selected_rows=[],  # <------------ no row is selected previously
        page_action="native",
        page_current=0,  # <------------ First page will be show
        page_size=25, # <------------  n of funds to be showed
        id='tabela-dash'
    )
    return table
                     

#---------------------------------------------------------------------------------------------------------------------------------------#

#  2. LAYOUT DEFINITION

        # 2.1 - dbc card for header of app
        # 2.2 - dbc.button for select what type of fund will be on table
        # 2.3 - Call function to insert data table

#---------------------------------------------------------------------------------------------------------------------------------------#


layout = html.Div([


#------------------------------------------------------- 2.1 ---------------------------------------------------------------------------#
        
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                            dbc.Card([dbc.CardHeader('Compare os melhores Fundos de Previdência', style={'textAlign':'center', 'fontWeight':'bold'})
                            ,
                            
#-------------------------------------------------------- 2.2 --------------------------------------------------------------------------#
                        #html.Div([
                            #dbc.Card([
                                #dbc.CardBody('Selecione a classificação CVM dos fundos na lista', style ={'textAlign': 'right'}
                
                       #         dbc.CardBody('teste', style ={'textAlign': 'left'}
                       #         )
                            
                        
                        
                    
                

#------------------------------------------------------- 2.2 --------------------------------------------------------------------------#

                    dbc.Col(
                        html.Div([
                            dbc.CardBody([
                            dbc.Button("Todos", color="warning", id='todos_button', n_clicks_timestamp='0'),
                            dbc.Button("Multimercados", color="light",id='multimercado_button', n_clicks_timestamp='0' ),
                            dbc.Button("Ações", color="warning", id='stocks_button', n_clicks_timestamp='0'),
                            dbc.Button("Renda Fixa", color="light", id='rf_button', n_clicks_timestamp='0')
                        ], style = {'textAlign':'right'}),
                        
                        ])
                    )
                            ])
                    ])

                ])

                        ])
]),
                

                #dcc.Dropdown(df['Indicator Name'].unique(), id = 'dropdown'),
                

#------------------------------------------------------- 2.3 --------------------------------------------------------------------------#
            dbc.Row([
                dbc.Col([
                    html.Div([
                        table_creation(dff), #calling the function with dff, but only will be displayed if the user use the button
                        
                    ], className="m-4 dbc")])
])
    ])

#---------------------------------------------------------------------------------------------------------------------------------------#

# 3 CALLBACK's

        # 3.1 - callback of buttons
        # 3.2 - modifying columns of dash.table_Datatable
        

#---------------------------------------------------------------------------------------------------------------------------------------#



#-------------------------------------------------------- 3.1 --------------------------------------------------------------------------#


@callback(Output('tabela-dash', 'data'),
              Input('multimercado_button','n_clicks_timestamp'),
              Input('stocks_button','n_clicks_timestamp'),
              Input('rf_button','n_clicks_timestamp'),
              Input('todos_button','n_clicks_timestamp')    
            )




def display(multimercado_button, stocks_button, rf_button, todos_button):

    
    if ctx.triggered != 'tabela-dash':
        if int(multimercado_button) > int(stocks_button) and int(multimercado_button) > int(rf_button) and int(multimercado_button) > int(todos_button): #Multimercado button

            value = 'Multimercado'

            db_filtered = pd.DataFrame(dff[dff['Classificação CVM'] == value])
            db_filtered = db_filtered.iloc[:,:9]
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')

            return db_filtered #<------------ Extracting data as dict, easy way to do


        elif int(stocks_button) > int(multimercado_button) and int(stocks_button) > int(rf_button) and int(stocks_button) > int(todos_button): #only button
            
            value = 'Ações'

            db_filtered = pd.DataFrame(dff[dff['Classificação CVM'] == value])
            db_filtered = db_filtered.iloc[:,:9]
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')


            
            return db_filtered#<------------ Extracting data as dict, easy way to do


        elif int(rf_button) > int(multimercado_button) and int(rf_button) > int(stocks_button) and int(rf_button) > int(todos_button): #biased button
            
            
            value = 'Renda Fixa'

            db_filtered = pd.DataFrame(dff[dff['Classificação CVM'] == value])
            db_filtered = db_filtered.iloc[:,:9]
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')


            
            return db_filtered#<------------ Extracting data as dict, easy way to do

        elif int(todos_button) > int(multimercado_button) and int(todos_button) > int(stocks_button) and int(todos_button) > int(rf_button): #Todos button
            
            db_filtered = pd.DataFrame(dff)
            db_filtered = db_filtered.iloc[:,:9]
            
            
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')


            
            return db_filtered#<------------ Extracting data as dict, easy way to do


        else:
            
            db_filtered = pd.DataFrame(dff)
            db_filtered = db_filtered.iloc[:,:9]
            
            db_filtered = db_filtered.to_dict('Records')

            
            return db_filtered #<------------ Extracting data as dict, easy way to do


#-------------------------------------------------------- 3.2 --------------------------------------------------------------------------#

#@app.callback(
#    Output('tabela-dash', 'columns'),
#    Input('dropdown', 'value'),
#    State('tabela-dash', 'columns')
#)
#def update_table(value, columns):
#    if value is None:
#        print('test 1: Value is None')
#    else:
#        print('test 1: Value is not None')


#    if columns is None:
#        print('test 2: Columns is None')
##    else:
 #       print('test 2: Columns in not None')#

#    columns = [columns[:2]]
#    columns = columns.append([{'name':value, 'id': value}])

    

 #   return columns



#--------------------------------------------------------------------------------------------------------------------------------------#

