import pandas as pd
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import Dash, Input, Output, callback_context as ctx, dash_table, callback, dcc
from dash_bootstrap_templates import load_figure_template
import base64





image_filename = r'https://github.com/glvieiraa/Watchlist_project/tree/main/data/logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode()




dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template('SOLAR')





app = dash.Dash(__name__, use_pages = True, external_stylesheets= [dbc.themes.SOLAR, dbc_css])
server = app.server



app.layout = html.Div(
    [
        html.Img(id='logo_png', src='data:image/png;base64,{}'.format((encoded_image)), style={'height':'8%', 'width':'8%','textAlign':'center'}),#<------------ Seeking BRA logo
        html.H2("Navegue usando os menus abaixo", style={'textAlign':'center'}),
        
    html.Div(
        [
            html.Div(
                dbc.Card([
                    dcc.Link(
                        f"{page['name']}", href=page["relative_path"])]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),                
                
    html.Hr(),
    dash.page_container,
            
                
    ]    
)
    

if __name__ == "__main__":
    app.run_server(debug=True)












