# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SendGeometry(Component):
    """A SendGeometry component.
Send geometry to a CAD Platform
geometry must be a single Display Geometry or Ladybug Geometry or a list of them

Keyword arguments:

- id (string; default 'po-send-geometry'):
    Unique ID to identify this component in Dash callbacks.

- defaultAction (a value equal to: 'add', 'delete', 'preview', 'clear', 'subscribe-preview'; default 'add')

- defaultKey (string; default 'send-pollination-geometry')

- geometry (list of strings; optional)

- geometryOptions (dict; optional)

    `geometryOptions` is a dict with keys:

    - units (a value equal to: 'Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters'; optional)

- optionsConfig (dict; optional)

    `optionsConfig` is a dict with keys:

    - add (boolean; required)

    - clear (boolean; required)

    - delete (boolean; required)

    - preview (boolean; required)

    - subscribe-preview (boolean; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'SendGeometry'
    @_explicitize_args
    def __init__(self, geometry=Component.UNDEFINED, defaultAction=Component.UNDEFINED, defaultKey=Component.UNDEFINED, optionsConfig=Component.UNDEFINED, geometryOptions=Component.UNDEFINED, onOverlayHeightChange=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'defaultAction', 'defaultKey', 'geometry', 'geometryOptions', 'optionsConfig']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'defaultAction', 'defaultKey', 'geometry', 'geometryOptions', 'optionsConfig']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SendGeometry, self).__init__(**args)
