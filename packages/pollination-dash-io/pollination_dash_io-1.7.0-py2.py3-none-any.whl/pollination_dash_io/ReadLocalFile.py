# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ReadLocalFile(Component):
    """A ReadLocalFile component.
Use this component to get user info

Keyword arguments:

- id (string; default 'po-get-file'):
    Unique ID to identify this component in Dash callbacks.

- filePath (string; required):
    Full path or relative path where the file is."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'ReadLocalFile'
    @_explicitize_args
    def __init__(self, filePath=Component.REQUIRED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'filePath']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'filePath']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['filePath']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ReadLocalFile, self).__init__(**args)
