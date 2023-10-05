# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SelectStudy(Component):
    """A SelectStudy component.
Use this component to get user info

Keyword arguments:

- id (string; default 'po-sel-study'):
    Unique ID to identify this component in Dash callbacks.

- accessToken (string; optional):
    JWT token.

- apiKey (string; optional):
    API key from Pollination Cloud.

- basePath (string; default 'https://api.pollination.cloud'):
    Base path of the API.

- projectName (string; default ''):
    Name of the project.

- projectOwner (string; default ''):
    Owner of the project.

- studyId (string; optional):
    Default ID of the study.

- value (dict; optional):
    Default cloud job.

    `value` is a dict with keys:

    - author (dict; optional):
        author @,type,{AccountPublic} @,memberof,CloudJob.

        `author` is a dict with keys:

        - account_type (string; required)

        - description (string; optional)

        - display_name (string; optional)

        - id (string; required)

        - name (string; required)

        - picture_url (string; optional):
            https://robohash.org/ladybugbot @,type,{string}
            @,memberof,AccountPublic.

    - id (string; required):
        The unique ID for this run @,type,{string}
        @,memberof,CloudJob.

    - owner (dict; optional):
        owner @,type,{AccountPublic} @,memberof,CloudJob.

        `owner` is a dict with keys:

        - account_type (string; required)

        - description (string; optional)

        - display_name (string; optional)

        - id (string; required)

        - name (string; required)

        - picture_url (string; optional):
            https://robohash.org/ladybugbot @,type,{string}
            @,memberof,AccountPublic.

    - recipe (dict; optional):
        The recipe used to generate this @,type,{RecipeInterface}
        @,memberof,CloudJob.

        `recipe` is a dict with keys:

        - annotations (dict with strings as keys and values of type string; optional):
            An optional dictionary to add annotations to inputs. These
            annotations will be used by the client side libraries.
            @,type,{{ [key: string]: string; }}
            @,memberof,RecipeInterface.

        - api_version (string; optional)

        - inputs (list of boolean | number | string | dict | lists; optional):
            A list of recipe inputs. @,type,{Array<DAGGenericInput |
            DAGStringInput | DAGIntegerInput | DAGNumberInput |
            DAGBooleanInput | DAGFolderInput | DAGFileInput |
            DAGPathInput | DAGArrayInput | DAGJSONObjectInput>}
            @,memberof,RecipeInterface.

        - metadata (dict; required):
            Recipe metadata information. @,type,{MetaData}
            @,memberof,RecipeInterface.

            `metadata` is a dict with keys:

            - annotations (dict with strings as keys and values of type string; optional):
                An optional dictionary to add annotations to inputs.
                These annotations will be used by the client side
                libraries. @,type,{{ [key: string]: string; }}
                @,memberof,MetaData.

            - app_version (string; optional):
                The version of the application code underlying the
                manifest @,type,{string} @,memberof,MetaData.

            - deprecated (boolean; optional):
                Whether this package is deprecated @,type,{boolean}
                @,memberof,MetaData.

            - description (string; optional):
                A description of what this package does
                @,type,{string} @,memberof,MetaData.

            - home (string; optional):
                The URL of this package\'s home page @,type,{string}
                @,memberof,MetaData.

            - icon (string; optional):
                A URL to an SVG or PNG image to be used as an icon
                @,type,{string} @,memberof,MetaData.

            - keywords (list of strings; optional):
                A list of keywords to search the package by
                @,type,{Array<string>} @,memberof,MetaData.

            - license (dict; optional):
                The license information. @,type,{License}
                @,memberof,MetaData.

                `license` is a dict with keys:

                - annotations (dict with strings as keys and values of type string; optional):
                    An optional dictionary to add annotations to
                    inputs. These annotations will be used by the
                    client side libraries. @,type,{{ [key: string]:
                    string; }} @,memberof,License.

                - name (string; required):
                    The license name used for the package.
                    @,type,{string} @,memberof,License.

                - type (string; optional)

                - url (string; optional):
                    A URL to the license used for the package.
                    @,type,{string} @,memberof,License.

            - maintainers (list of dicts; optional):
                A list of maintainers for the package
                @,type,{Array<Maintainer>} @,memberof,MetaData.

                `maintainers` is a list of dicts with keys:

    - annotations (dict with strings as keys and values of type string; optional):
        An optional dictionary to add annotations to inputs. These
        annotations will be used by the client side libraries.
        @,type,{{ [key: string]: string; }} @,memberof,Maintainer.

    - email (string; optional):
        The email address of the author/maintainer person or
        organization. @,type,{string} @,memberof,Maintainer.

    - name (string; required):
        The name of the author/maintainer person or organization.
        @,type,{string} @,memberof,Maintainer.

    - type (string; optional)

            - name (string; required):
                Package name. Make it descriptive and helpful ;)
                @,type,{string} @,memberof,MetaData.

            - sources (list of strings; optional):
                A list of URLs to source code for this project
                @,type,{Array<string>} @,memberof,MetaData.

            - tag (string; required):
                The tag of the package @,type,{string}
                @,memberof,MetaData.

            - type (string; optional)

        - outputs (list of boolean | number | string | dict | lists; optional):
            A list of recipe outputs. @,type,{Array<DAGGenericOutput |
            DAGStringOutput | DAGIntegerOutput | DAGNumberOutput |
            DAGBooleanOutput | DAGFolderOutput | DAGFileOutput |
            DAGPathOutput | DAGArrayOutput | DAGJSONObjectOutput>}
            @,memberof,RecipeInterface.

        - source (string; optional):
            A URL to the source this recipe from a registry.
            @,type,{string} @,memberof,RecipeInterface.

        - type (string; optional)

    - resources_duration (dict; optional):
        CPU and Memory usage aggregated for all runs in this job
        @,type,{ResourcesDuration} @,memberof,CloudJob.

        `resources_duration` is a dict with keys:

        - cpu (number; optional)

        - memory (number; optional)

    - spec (dict; required):
        The job specification @,type,{Job} @,memberof,CloudJob.

        `spec` is a dict with keys:

        - annotations (dict with strings as keys and values of type string; optional):
            An optional dictionary to add annotations to inputs. These
            annotations will be used by the client side libraries.
            @,type,{{ [key: string]: string; }} @,memberof,Job.

        - api_version (string; optional)

        - arguments (list of list of boolean | number | string | dict | listss; optional):
            Input arguments for this job.
            @,type,{Array<Array<JobArgument | JobPathArgument>>}
            @,memberof,Job.

        - description (string; optional):
            Run description. @,type,{string} @,memberof,Job.

        - labels (dict with strings as keys and values of type string; optional):
            Optional user data as a dictionary. User data is for user
            reference only and will not be used in the execution of
            the job. @,type,{{ [key: string]: string; }}
            @,memberof,Job.

        - name (string; optional):
            An optional name for this job. This name will be used a
            the display name for the run. @,type,{string}
            @,memberof,Job.

        - source (string; required):
            The source url for downloading the recipe. @,type,{string}
            @,memberof,Job.

        - type (string; optional)

    - status (dict; optional):
        The status of the job @,type,{JobStatus} @,memberof,CloudJob.

        `status` is a dict with keys:

        - annotations (dict with strings as keys and values of type string; optional):
            An optional dictionary to add annotations to inputs. These
            annotations will be used by the client side libraries.
            @,type,{{ [key: string]: string; }} @,memberof,JobStatus.

        - api_version (string; optional)

        - finished_at (string; optional):
            The time at which the task was completed @,type,{string}
            @,memberof,JobStatus.

        - id (string; required):
            The ID of the individual job. @,type,{string}
            @,memberof,JobStatus.

        - message (string; optional):
            Any message produced by the job. Usually error/debugging
            hints. @,type,{string} @,memberof,JobStatus.

        - runs_cancelled (number; optional):
            The count of runs that have been cancelled @,type,{number}
            @,memberof,JobStatus.

        - runs_completed (number; optional):
            The count of runs that have completed @,type,{number}
            @,memberof,JobStatus.

        - runs_failed (number; optional):
            The count of runs that have failed @,type,{number}
            @,memberof,JobStatus.

        - runs_pending (number; optional):
            The count of runs that are pending @,type,{number}
            @,memberof,JobStatus.

        - runs_running (number; optional):
            The count of runs that are running @,type,{number}
            @,memberof,JobStatus.

        - source (string; optional):
            Source url for the status object. It can be a recipe or a
            function. @,type,{string} @,memberof,JobStatus.

        - started_at (string; required):
            The time at which the job was started @,type,{string}
            @,memberof,JobStatus.

        - status (a value equal to: 'Created', 'Pre-Processing', 'Running', 'Failed', 'Cancelled', 'Completed', 'Unknown'; optional):
            The status of this job. @,type,{JobStatusEnum}
            @,memberof,JobStatus.

        - type (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'SelectStudy'
    @_explicitize_args
    def __init__(self, projectOwner=Component.UNDEFINED, projectName=Component.UNDEFINED, studyId=Component.UNDEFINED, value=Component.UNDEFINED, accessToken=Component.UNDEFINED, apiKey=Component.UNDEFINED, basePath=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessToken', 'apiKey', 'basePath', 'projectName', 'projectOwner', 'studyId', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessToken', 'apiKey', 'basePath', 'projectName', 'projectOwner', 'studyId', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SelectStudy, self).__init__(**args)
