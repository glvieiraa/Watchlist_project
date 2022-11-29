
#----------------------------------------Importing libraries----------------------------------------------------------# 
import pandas as pd
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import Dash, Input, Output, callback_context as ctx, dash_table, callback
from dash_bootstrap_templates import load_figure_template
import base64



#--------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------Importing components and data----------------------------------------------------------#



#Importing dataframes, altering format style, importing images and templates


df = pd.DataFrame(pd.read_excel(r'C:\Users\Gustavo.vieira\Desktop\python\estudos_dash\watchlist_project\data\Acompanhamento Fundos.xlsx', sheet_name= 'Todos', header = 1))
dff= pd.DataFrame(df[['Nome','tipo','retorno no mês','retorno no ano', 'retorno 12 meses','retorno 24 meses', 'retorno 36 meses', 'retorno desde o inicio', 'volatilidade 12 meses', 'Indicator Name']]).copy()
start_df = pd.DataFrame(dff[['Nome','tipo','retorno no mês','retorno no ano', 'retorno 12 meses']])

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


#---------------------------------------------------------------------------------------------------------------------------------------#

#  1. FUNCTIONS CONSTRUCTION

        # 1.1 - table_creation
            

#---------------------------------------------------------------------------------------------------------------------------------------#

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
        id='tabela-dash-fundos'
    )
    return table

                     

#---------------------------------------------------------------------------------------------------------------------------------------#

#  2. LAYOUT DEFINITION

        # 2.1 - dbc card for header of app
        # 2.2 - dbc.button for select what type of fund will be on table
            # 2.2.1 - Cardheader of page select
            # 2.2.2 - dcc buttons
        # 2.3 - Call function to insert data table

#---------------------------------------------------------------------------------------------------------------------------------------#

dash.register_page(__name__)



layout = html.Div([


#------------------------------------------------------- 2.1 ---------------------------------------------------------------------------#
        
         dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                            dbc.Card([dbc.CardHeader('Compare os melhores Fundos de investimento', style={'textAlign':'center', 'fontWeight':'bold'})
                            ,
                            
#-------------------------------------------------------- 2.2.1--------------------------------------------------------------------------#
                      

#------------------------------------------------------- 2.2.2  --------------------------------------------------------------------------#

    dbc.CardBody([
                            dbc.Button("Todos", color="warning", id='todos_button', n_clicks_timestamp='0'),
                            dbc.Button("Multimercados", color="light",id='multimercado_button', n_clicks_timestamp='0' ),
                            dbc.Button("Long only", color="warning", id='only_button', n_clicks_timestamp='0'),
                            dbc.Button("Long Biased", color="light", id='biased_button', n_clicks_timestamp='0')
                        ], style = {'textAlign':'right'}),
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
                            
                        ], className="m-4 dbc")
                    ])
            ])
])
        
            
    

        


#---------------------------------------------------------------------------------------------------------------------------------------#

# 3 CALLBACK's

        # 3.1 - callback of buttons
        # 3.2 - modifying columns of dash.table_Datatable
        

#---------------------------------------------------------------------------------------------------------------------------------------#



#-------------------------------------------------------- 3.1 --------------------------------------------------------------------------#


@callback(Output('tabela-dash-fundos', 'data'),
            Input('multimercado_button','n_clicks_timestamp'),
            Input('only_button','n_clicks_timestamp'),
            Input('biased_button','n_clicks_timestamp'),
            Input('todos_button','n_clicks_timestamp')    
            )




def display(multimercado_button, only_button, biased_button, todos_button):

    
    if ctx.triggered != 'tabela-dash-fundos':
        if int(multimercado_button) > int(only_button) and int(multimercado_button) > int(biased_button) and int(multimercado_button) > int(todos_button): #Multimercado button

            value = 'Multimercado'

            db_filtered = pd.DataFrame(dff[dff['tipo'] == value]) #Filtering just Funds class of interest, in this case, Multimercado Funds (value variable)
            db_filtered = db_filtered.iloc[:,:9] #Selecting our first 9 columns
            print(db_filtered) #Confirming data
            db_filtered = db_filtered.to_dict('Records') # converting data as dict, easy way to pass for tabl_creation

            return db_filtered #<------------ ( SAME ENGINE FOR ALL BUTTONS )


        elif int(only_button) > int(multimercado_button) and int(only_button) > int(biased_button) and int(only_button) > int(todos_button): #only button
            
            value = 'Long Only'

            db_filtered = pd.DataFrame(dff[dff['tipo'] == value])
            db_filtered = db_filtered.iloc[:,:9]
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')


            
            return db_filtered


        elif int(biased_button) > int(multimercado_button) and int(biased_button) > int(only_button) and int(biased_button) > int(todos_button): #biased button
            
            
            value = 'Long Biased'

            db_filtered = pd.DataFrame(dff[dff['tipo'] == value])
            db_filtered = db_filtered.iloc[:,:9]
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')


            
            return db_filtered

        elif int(todos_button) > int(multimercado_button) and int(todos_button) > int(only_button) and int(todos_button) > int(biased_button): #Todos button
            
            db_filtered = pd.DataFrame(dff)
            db_filtered = db_filtered.iloc[:,:9]
            
            
            print(db_filtered)
            db_filtered = db_filtered.to_dict('Records')


            
            return db_filtered


        else:
            
            db_filtered = pd.DataFrame(dff)
            db_filtered = db_filtered.iloc[:,:9]
            
            db_filtered = db_filtered.to_dict('Records')

            
            return db_filtered


#-------------------------------------------------------- 3.2 --------------------------------------------------------------------------#

#@app.callback(
#    Output('tabela-dash-fundos', 'columns'),
#    Input('dropdown', 'value'),
#    State('tabela-dash-fundos', 'columns')
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

