import dash_renderjson
import pollination_dash_io
import dash
from dash import html
from dash.dependencies import Input, Output
import dash_daq as daq

# declare the app
app = dash.Dash(__name__)

app.layout = html.Div([
    pollination_dash_io.GetHbjson(id='my-model', 
                                  optionsConfig={ 
                                      "subscribe": { "show": True, "selected": True }, 
                                      "selection": { "show": True, "selected": False }}, 
                                  buttonLabel='Get Rhino Model',
                                  defaultKey='my-model',
                                  useIcon=True,
                                  fullWidth=True),
    daq.BooleanSwitch(id='try-selector', on=False, label='Change settings'),
    daq.BooleanSwitch(id='try-icon', on=False, label='Use icon?'),
    daq.BooleanSwitch(id='try-full-width', on=False, label='Full width?'),
    html.Div(id='output'),
])

# TODO: fix get model component
@app.callback(Output('my-model', 'optionsConfig'),
              Input('try-selector', 'on'))
def try_selector(on):
    return { 
        "subscribe": { "show": True, "selected": True }, 
        "selection": { "show": True, "selected": on }}

@app.callback(Output('my-model', 'useIcon'),
              Input('try-icon', 'on'))
def try_icon(on):
    return on

@app.callback(Output('my-model', 'fullWidth'),
              Input('try-full-width', 'on'))
def try_full_width(on):
    return on

@app.callback(
    Output(component_id='output',
      component_property='children'),
    Input(component_id='my-model',
      component_property='hbjson')
)
def get_value_from_recipe_form(data):
    return dash_renderjson.DashRenderjson(id='json-out',
                                          data=data)

if __name__ == '__main__':
    app.run_server(debug=True)
