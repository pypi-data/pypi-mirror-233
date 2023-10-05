# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SendHbjson(Component):
    """A SendHbjson component.
Send a HBJSON model to a CAD Platform
hbjson must be a valid HBJSON model

Keyword arguments:

- id (string; default 'po-send-hbjson'):
    Unique ID to identify this component in Dash callbacks.

- defaultAction (a value equal to: 'add', 'delete', 'preview', 'clear', 'subscribe-preview', 'replace'; default 'add')

- defaultKey (string; default 'send-pollination-model')

- hbjson (dict; optional)

- optionsConfig (dict; optional)

    `optionsConfig` is a dict with keys:

    - add (boolean; required)

    - clear (boolean; required)

    - delete (boolean; required)

    - preview (boolean; required)

    - replace (boolean; required)

    - subscribe-preview (boolean; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'SendHbjson'
    @_explicitize_args
    def __init__(self, hbjson=Component.UNDEFINED, defaultAction=Component.UNDEFINED, defaultKey=Component.UNDEFINED, optionsConfig=Component.UNDEFINED, onOverlayHeightChange=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'defaultAction', 'defaultKey', 'hbjson', 'optionsConfig']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'defaultAction', 'defaultKey', 'hbjson', 'optionsConfig']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SendHbjson, self).__init__(**args)
