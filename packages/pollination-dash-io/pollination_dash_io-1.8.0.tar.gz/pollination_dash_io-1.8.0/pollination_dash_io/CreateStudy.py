# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CreateStudy(Component):
    """A CreateStudy component.
Use this component to run studies

State
- study (dictionary; it has following info):
   accountName
   projectName
   studyId
   run
   isLocal
   refreshKey

Keyword arguments:

- id (string; default 'po-create-study'):
    Unique ID to identify this component in Dash callbacks.

- accessToken (string; optional):
    JWT token.

- apiKey (string; default ''):
    API key from Pollination Cloud.

- basePath (string; default 'https://api.pollination.cloud'):
    Base path of the API."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'CreateStudy'
    @_explicitize_args
    def __init__(self, accessToken=Component.UNDEFINED, apiKey=Component.UNDEFINED, basePath=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessToken', 'apiKey', 'basePath']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessToken', 'apiKey', 'basePath']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(CreateStudy, self).__init__(**args)
