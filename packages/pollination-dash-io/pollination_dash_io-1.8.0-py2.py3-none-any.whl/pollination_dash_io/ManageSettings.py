# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ManageSettings(Component):
    """A ManageSettings component.
Use this component to get the host name

Keyword arguments:

- id (string; default 'po-manage-settings'):
    Unique ID to identify this component in Dash callbacks.

- settings (dict; default undefined):
    Settings to apply.

    `settings` is a dict with keys:

    - angle_tolerance (number; required)

    - layers (list of strings; required)

    - location (dict; required)

        `location` is a dict with keys:

        - city (string; required)

        - elevation (number; required)

        - latitude (number; required)

        - longitude (number; required)

        - time_zone (number; required)

    - tolerance (number; required)

    - units (a value equal to: 'Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters'; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'ManageSettings'
    @_explicitize_args
    def __init__(self, settings=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'settings']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'settings']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ManageSettings, self).__init__(**args)
