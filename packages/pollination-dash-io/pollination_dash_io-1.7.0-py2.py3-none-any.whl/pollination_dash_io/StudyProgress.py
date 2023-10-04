# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class StudyProgress(Component):
    """A StudyProgress component.
Use this component to keep track of a study and get its results
If you click on a file card you get data as base64 string

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- accessToken (string; optional):
    JWT token.

- apiKey (string; default ''):
    API key from Pollination Cloud.

- basePath (string; default 'https://api.pollination.cloud'):
    Base path of the API.

- color (string; default '#1890ff'):
    Progress bar color.

- isLocal (boolean; optional):
    Start as local simulation.

- projectName (string; default ''):
    Name of the project.

- projectOwner (string; default ''):
    Owner of the project.

- refreshInterval (number; default 400):
    Refresh interval in milliseconds.

- run (dict; required):
    Run or Local run to fetch.

    `run` is a dict with keys:

    - author (dict; optional):
        author @,type,{AccountPublic} @,memberof,Run.

        `author` is a dict with keys:

        - account_type (string; required)

        - description (string; optional)

        - display_name (string; optional)

        - id (string; required)

        - name (string; required)

        - picture_url (string; optional):
            https://robohash.org/ladybugbot @,type,{string}
            @,memberof,AccountPublic.

    - generation (number; optional):
        The generation of this run @,type,{number} @,memberof,Run.

    - id (string; required):
        The unique ID for this run @,type,{string} @,memberof,Run.

    - meta (dict; optional):
        Extra metadata about the run @,type,{RunMeta} @,memberof,Run.

        `meta` is a dict with keys:

        - progress (dict; optional):
            progress of the run @,type,{RunProgress}
            @,memberof,RunMeta.

            `progress` is a dict with keys:

            - completed (number; optional)

            - running (number; optional)

            - total (number; optional)

        - resources_duration (dict; optional):
            resource usage @,type,{ResourcesDuration}
            @,memberof,RunMeta.

            `resources_duration` is a dict with keys:

            - cpu (number; optional)

            - memory (number; optional)

    - owner (dict; optional):
        owner @,type,{AccountPublic} @,memberof,Run.

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
        @,memberof,Run.

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

    - status (dict; optional):
        The status of the run @,type,{RunStatus} @,memberof,Run.

        `status` is a dict with keys:

        - annotations (dict with strings as keys and values of type string; optional):
            An optional dictionary to add annotations to inputs. These
            annotations will be used by the client side libraries.
            @,type,{{ [key: string]: string; }} @,memberof,RunStatus.

        - api_version (string; optional)

        - entrypoint (string; optional):
            The ID of the first step in the run. @,type,{string}
            @,memberof,RunStatus.

        - finished_at (string; optional):
            The time at which the task was completed @,type,{string}
            @,memberof,RunStatus.

        - id (string; required):
            The ID of the individual run. @,type,{string}
            @,memberof,RunStatus.

        - inputs (list of boolean | number | string | dict | lists; required):
            The inputs used for this run.
            @,type,{Array<StepStringInput | StepIntegerInput |
            StepNumberInput | StepBooleanInput | StepFolderInput |
            StepFileInput | StepPathInput | StepArrayInput |
            StepJSONObjectInput>} @,memberof,RunStatus.

        - job_id (string; required):
            The ID of the job that generated this run. @,type,{string}
            @,memberof,RunStatus.

        - message (string; optional):
            Any message produced by the task. Usually error/debugging
            hints. @,type,{string} @,memberof,RunStatus.

        - outputs (list of boolean | number | string | dict | lists; required):
            The outputs produced by this run.
            @,type,{Array<StepStringOutput | StepIntegerOutput |
            StepNumberOutput | StepBooleanOutput | StepFolderOutput |
            StepFileOutput | StepPathOutput | StepArrayOutput |
            StepJSONObjectOutput>} @,memberof,RunStatus.

        - source (string; optional):
            Source url for the status object. It can be a recipe or a
            function. @,type,{string} @,memberof,RunStatus.

        - started_at (string; required):
            The time at which the task was started @,type,{string}
            @,memberof,RunStatus.

        - status (a value equal to: 'Created', 'Scheduled', 'Running', 'Post-Processing', 'Failed', 'Cancelled', 'Succeeded', 'Unknown'; optional):
            The status of this run. @,type,{RunStatusEnum}
            @,memberof,RunStatus.

        - steps (dict; optional)

            `steps` is a dict with strings as keys and values of type
            dict with keys:

    - annotations (dict with strings as keys and values of type string; optional):
        An optional dictionary to add annotations to inputs. These
        annotations will be used by the client side libraries.
        @,type,{{ [key: string]: string; }} @,memberof,StepStatus.

    - boundary_id (string; optional):
        This indicates the step ID of the associated template root
        step in which this step belongs to. A DAG step will have the
        id of the             parent DAG for example. @,type,{string}
        @,memberof,StepStatus.

    - children_ids (list of strings; required):
        A list of child step IDs @,type,{Array<string>}
        @,memberof,StepStatus.

    - command (string; optional):
        The command used to run this step. Only applies to Function
        steps. @,type,{string} @,memberof,StepStatus.

    - finished_at (string; optional):
        The time at which the task was completed @,type,{string}
        @,memberof,StepStatus.

    - id (string; required):
        The step unique ID @,type,{string} @,memberof,StepStatus.

    - inputs (list of boolean | number | string | dict | lists; required):
        The inputs used by this step. @,type,{Array<StepStringInput |
        StepIntegerInput | StepNumberInput | StepBooleanInput |
        StepFolderInput | StepFileInput | StepPathInput |
        StepArrayInput | StepJSONObjectInput>} @,memberof,StepStatus.

    - message (string; optional):
        Any message produced by the task. Usually error/debugging
        hints. @,type,{string} @,memberof,StepStatus.

    - name (string; required):
        A human readable name for the step. Usually defined by the DAG
        task name but can be extended if the step is part of a loop
        for example. This name is unique within the boundary of the
        DAG/Job that generated it. @,type,{string}
        @,memberof,StepStatus.

    - outbound_steps (list of strings; required):
        A list of the last step to ran in the context of this step. In
        the case of a DAG or a job this will be the last step that has
        been executed. It will remain empty for functions.
        @,type,{Array<string>} @,memberof,StepStatus.

    - outputs (list of boolean | number | string | dict | lists; required):
        The outputs produced by this step.
        @,type,{Array<StepStringOutput | StepIntegerOutput |
        StepNumberOutput | StepBooleanOutput | StepFolderOutput |
        StepFileOutput | StepPathOutput | StepArrayOutput |
        StepJSONObjectOutput>} @,memberof,StepStatus.

    - source (string; optional):
        Source url for the status object. It can be a recipe or a
        function. @,type,{string} @,memberof,StepStatus.

    - started_at (string; required):
        The time at which the task was started @,type,{string}
        @,memberof,StepStatus.

    - status (a value equal to: 'Scheduled', 'Running', 'Failed', 'Succeeded', 'Skipped', 'Unknown'; optional):
        The status of this step. @,type,{StepStatusEnum}
        @,memberof,StepStatus.

    - status_type (a value equal to: 'Function', 'DAG', 'Loop', 'Container', 'Unknown'; required):
        The type of step this status is for. Can be \\"Function\\",
        \\"DAG\\" or \\"Loop\\" @,type,{StatusType}
        @,memberof,StepStatus.

    - template_ref (string; required):
        The name of the template that spawned this step
        @,type,{string} @,memberof,StepStatus.

    - type (string; optional)

        - type (string; optional)

- showOutput (boolean; default True):
    Show inputs and outputs.

- showResult (boolean; optional):
    Show visualization set of a CardFile directly.

- showStatusLabel (boolean; default False):
    Show status label."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'StudyProgress'
    @_explicitize_args
    def __init__(self, projectOwner=Component.UNDEFINED, projectName=Component.UNDEFINED, run=Component.REQUIRED, isLocal=Component.UNDEFINED, showResult=Component.UNDEFINED, showOutput=Component.UNDEFINED, refreshInterval=Component.UNDEFINED, color=Component.UNDEFINED, showStatusLabel=Component.UNDEFINED, accessToken=Component.UNDEFINED, apiKey=Component.UNDEFINED, basePath=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessToken', 'apiKey', 'basePath', 'color', 'isLocal', 'projectName', 'projectOwner', 'refreshInterval', 'run', 'showOutput', 'showResult', 'showStatusLabel']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessToken', 'apiKey', 'basePath', 'color', 'isLocal', 'projectName', 'projectOwner', 'refreshInterval', 'run', 'showOutput', 'showResult', 'showStatusLabel']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['run']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(StudyProgress, self).__init__(**args)
