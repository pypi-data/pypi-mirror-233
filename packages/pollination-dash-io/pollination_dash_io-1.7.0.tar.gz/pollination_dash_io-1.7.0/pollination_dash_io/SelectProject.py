# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SelectProject(Component):
    """A SelectProject component.
Use this component to get user info

Keyword arguments:

- id (string; default 'po-sel-project'):
    Unique ID to identify this component in Dash callbacks.

- accessToken (string; optional):
    JWT token.

- apiKey (string; optional):
    API key from Pollination Cloud.

- basePath (string; default 'https://api.pollination.cloud'):
    Base path of the API.

- defaultProjectId (string; optional):
    Default project.

- projectOwner (string; default ''):
    Owner of the project."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'SelectProject'
    @_explicitize_args
    def __init__(self, projectOwner=Component.UNDEFINED, defaultProjectId=Component.UNDEFINED, accessToken=Component.UNDEFINED, apiKey=Component.UNDEFINED, basePath=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessToken', 'apiKey', 'basePath', 'defaultProjectId', 'projectOwner']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessToken', 'apiKey', 'basePath', 'defaultProjectId', 'projectOwner']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SelectProject, self).__init__(**args)
