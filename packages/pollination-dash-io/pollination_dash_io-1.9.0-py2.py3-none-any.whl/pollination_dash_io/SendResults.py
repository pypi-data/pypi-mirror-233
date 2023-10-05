# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SendResults(Component):
    """A SendResults component.
Send a visualization set to a CAD Platform
results must be a valid HBJSON model

Keyword arguments:

- id (string; default 'po-send-results'):
    Unique ID to identify this component in Dash callbacks.

- defaultAction (a value equal to: 'add', 'delete', 'preview', 'clear', 'subscribe-preview'; default 'add')

- defaultKey (string; default 'send-pollination-results')

- delay (number; default 100)

- geometryOptions (dict; optional)

    `geometryOptions` is a dict with keys:

    - units (a value equal to: 'Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters'; optional)

- optionsConfig (dict; optional)

    `optionsConfig` is a dict with keys:

    - add (boolean; required)

    - clear (boolean; required)

    - delete (boolean; required)

    - preview (boolean; required)

    - subscribe-preview (boolean; required)

- results (boolean | number | string | dict | list; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'SendResults'
    @_explicitize_args
    def __init__(self, results=Component.UNDEFINED, defaultAction=Component.UNDEFINED, defaultKey=Component.UNDEFINED, optionsConfig=Component.UNDEFINED, geometryOptions=Component.UNDEFINED, onOverlayHeightChange=Component.UNDEFINED, delay=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'defaultAction', 'defaultKey', 'delay', 'geometryOptions', 'optionsConfig', 'results']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'defaultAction', 'defaultKey', 'delay', 'geometryOptions', 'optionsConfig', 'results']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SendResults, self).__init__(**args)
