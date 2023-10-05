# AUTO GENERATED FILE - DO NOT EDIT

export ''_studyprogress

"""
    ''_studyprogress(;kwargs...)

A StudyProgress component.
Use this component to keep track of a study and get its results
If you click on a file card you get data as base64 string
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
- `color` (String; optional): Progress bar color
- `isLocal` (Bool; optional): Start as local simulation
- `projectName` (String; optional): Name of the project
- `projectOwner` (String; optional): Owner of the project
- `refreshInterval` (Real; optional): Refresh interval in milliseconds
- `run` (required): Run or Local run to fetch. run has the following type: lists containing elements 'author', 'generation', 'id', 'meta', 'owner', 'recipe', 'status'.
Those elements have the following types:
  - `author` (optional): author
@,type,{AccountPublic}
@,memberof,Run. author has the following type: lists containing elements 'account_type', 'description', 'display_name', 'id', 'name', 'picture_url'.
Those elements have the following types:
  - `account_type` (String; required)
  - `description` (String; optional)
  - `display_name` (String; optional)
  - `id` (String; required)
  - `name` (String; required)
  - `picture_url` (String; optional): https://robohash.org/ladybugbot
@,type,{string}
@,memberof,AccountPublic
  - `generation` (Real; optional): The generation of this run
@,type,{number}
@,memberof,Run
  - `id` (String; required): The unique ID for this run
@,type,{string}
@,memberof,Run
  - `meta` (optional): Extra metadata about the run
@,type,{RunMeta}
@,memberof,Run. meta has the following type: lists containing elements 'progress', 'resources_duration'.
Those elements have the following types:
  - `progress` (optional): progress of the run
@,type,{RunProgress}
@,memberof,RunMeta. progress has the following type: lists containing elements 'completed', 'running', 'total'.
Those elements have the following types:
  - `completed` (Real; optional)
  - `running` (Real; optional)
  - `total` (Real; optional)
  - `resources_duration` (optional): resource usage
@,type,{ResourcesDuration}
@,memberof,RunMeta. resources_duration has the following type: lists containing elements 'cpu', 'memory'.
Those elements have the following types:
  - `cpu` (Real; optional)
  - `memory` (Real; optional)
  - `owner` (optional): owner
@,type,{AccountPublic}
@,memberof,Run. owner has the following type: lists containing elements 'account_type', 'description', 'display_name', 'id', 'name', 'picture_url'.
Those elements have the following types:
  - `account_type` (String; required)
  - `description` (String; optional)
  - `display_name` (String; optional)
  - `id` (String; required)
  - `name` (String; required)
  - `picture_url` (String; optional): https://robohash.org/ladybugbot
@,type,{string}
@,memberof,AccountPublic
  - `recipe` (optional): The recipe used to generate this
@,type,{RecipeInterface}
@,memberof,Run. recipe has the following type: lists containing elements 'annotations', 'api_version', 'inputs', 'metadata', 'outputs', 'source', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,RecipeInterface
  - `api_version` (String; optional)
  - `inputs` (Array of Bool | Real | String | Dict | Arrays; optional): A list of recipe inputs.
@,type,{Array<DAGGenericInput | DAGStringInput | DAGIntegerInput | DAGNumberInput | DAGBooleanInput | DAGFolderInput | DAGFileInput | DAGPathInput | DAGArrayInput | DAGJSONObjectInput>}
@,memberof,RecipeInterface
  - `metadata` (required): Recipe metadata information.
@,type,{MetaData}
@,memberof,RecipeInterface. metadata has the following type: lists containing elements 'annotations', 'app_version', 'deprecated', 'description', 'home', 'icon', 'keywords', 'license', 'maintainers', 'name', 'sources', 'tag', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,MetaData
  - `app_version` (String; optional): The version of the application code underlying the manifest
@,type,{string}
@,memberof,MetaData
  - `deprecated` (Bool; optional): Whether this package is deprecated
@,type,{boolean}
@,memberof,MetaData
  - `description` (String; optional): A description of what this package does
@,type,{string}
@,memberof,MetaData
  - `home` (String; optional): The URL of this package\'s home page
@,type,{string}
@,memberof,MetaData
  - `icon` (String; optional): A URL to an SVG or PNG image to be used as an icon
@,type,{string}
@,memberof,MetaData
  - `keywords` (Array of Strings; optional): A list of keywords to search the package by
@,type,{Array<string>}
@,memberof,MetaData
  - `license` (optional): The license information.
@,type,{License}
@,memberof,MetaData. license has the following type: lists containing elements 'annotations', 'name', 'type', 'url'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,License
  - `name` (String; required): The license name used for the package.
@,type,{string}
@,memberof,License
  - `type` (String; optional)
  - `url` (String; optional): A URL to the license used for the package.
@,type,{string}
@,memberof,License
  - `maintainers` (optional): A list of maintainers for the package
@,type,{Array<Maintainer>}
@,memberof,MetaData. maintainers has the following type: Array of lists containing elements 'annotations', 'email', 'name', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,Maintainer
  - `email` (String; optional): The email address of the author/maintainer person or organization.
@,type,{string}
@,memberof,Maintainer
  - `name` (String; required): The name of the author/maintainer person or organization.
@,type,{string}
@,memberof,Maintainer
  - `type` (String; optional)s
  - `name` (String; required): Package name. Make it descriptive and helpful ;)
@,type,{string}
@,memberof,MetaData
  - `sources` (Array of Strings; optional): A list of URLs to source code for this project
@,type,{Array<string>}
@,memberof,MetaData
  - `tag` (String; required): The tag of the package
@,type,{string}
@,memberof,MetaData
  - `type` (String; optional)
  - `outputs` (Array of Bool | Real | String | Dict | Arrays; optional): A list of recipe outputs.
@,type,{Array<DAGGenericOutput | DAGStringOutput | DAGIntegerOutput | DAGNumberOutput | DAGBooleanOutput | DAGFolderOutput | DAGFileOutput | DAGPathOutput | DAGArrayOutput | DAGJSONObjectOutput>}
@,memberof,RecipeInterface
  - `source` (String; optional): A URL to the source this recipe from a registry.
@,type,{string}
@,memberof,RecipeInterface
  - `type` (String; optional)
  - `status` (optional): The status of the run
@,type,{RunStatus}
@,memberof,Run. status has the following type: lists containing elements 'annotations', 'api_version', 'entrypoint', 'finished_at', 'id', 'inputs', 'job_id', 'message', 'outputs', 'source', 'started_at', 'status', 'steps', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,RunStatus
  - `api_version` (String; optional)
  - `entrypoint` (String; optional): The ID of the first step in the run.
@,type,{string}
@,memberof,RunStatus
  - `finished_at` (String; optional): The time at which the task was completed
@,type,{string}
@,memberof,RunStatus
  - `id` (String; required): The ID of the individual run.
@,type,{string}
@,memberof,RunStatus
  - `inputs` (Array of Bool | Real | String | Dict | Arrays; required): The inputs used for this run.
@,type,{Array<StepStringInput | StepIntegerInput | StepNumberInput | StepBooleanInput | StepFolderInput | StepFileInput | StepPathInput | StepArrayInput | StepJSONObjectInput>}
@,memberof,RunStatus
  - `job_id` (String; required): The ID of the job that generated this run.
@,type,{string}
@,memberof,RunStatus
  - `message` (String; optional): Any message produced by the task. Usually error/debugging hints.
@,type,{string}
@,memberof,RunStatus
  - `outputs` (Array of Bool | Real | String | Dict | Arrays; required): The outputs produced by this run.
@,type,{Array<StepStringOutput | StepIntegerOutput | StepNumberOutput | StepBooleanOutput | StepFolderOutput | StepFileOutput | StepPathOutput | StepArrayOutput | StepJSONObjectOutput>}
@,memberof,RunStatus
  - `source` (String; optional): Source url for the status object. It can be a recipe or a function.
@,type,{string}
@,memberof,RunStatus
  - `started_at` (String; required): The time at which the task was started
@,type,{string}
@,memberof,RunStatus
  - `status` (a value equal to: 'Created', 'Scheduled', 'Running', 'Post-Processing', 'Failed', 'Cancelled', 'Succeeded', 'Unknown'; optional): The status of this run.
@,type,{RunStatusEnum}
@,memberof,RunStatus
  - `steps` (optional): . steps has the following type: Dict with Strings as keys and values of type lists containing elements 'annotations', 'boundary_id', 'children_ids', 'command', 'finished_at', 'id', 'inputs', 'message', 'name', 'outbound_steps', 'outputs', 'source', 'started_at', 'status', 'status_type', 'template_ref', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,StepStatus
  - `boundary_id` (String; optional): This indicates the step ID of the associated template root             step in which this step belongs to. A DAG step will have the id of the             parent DAG for example.
@,type,{string}
@,memberof,StepStatus
  - `children_ids` (Array of Strings; required): A list of child step IDs
@,type,{Array<string>}
@,memberof,StepStatus
  - `command` (String; optional): The command used to run this step. Only applies to Function steps.
@,type,{string}
@,memberof,StepStatus
  - `finished_at` (String; optional): The time at which the task was completed
@,type,{string}
@,memberof,StepStatus
  - `id` (String; required): The step unique ID
@,type,{string}
@,memberof,StepStatus
  - `inputs` (Array of Bool | Real | String | Dict | Arrays; required): The inputs used by this step.
@,type,{Array<StepStringInput | StepIntegerInput | StepNumberInput | StepBooleanInput | StepFolderInput | StepFileInput | StepPathInput | StepArrayInput | StepJSONObjectInput>}
@,memberof,StepStatus
  - `message` (String; optional): Any message produced by the task. Usually error/debugging hints.
@,type,{string}
@,memberof,StepStatus
  - `name` (String; required): A human readable name for the step. Usually defined by the DAG task name but can be extended if the step is part of a loop for example. This name is unique within the boundary of the DAG/Job that generated it.
@,type,{string}
@,memberof,StepStatus
  - `outbound_steps` (Array of Strings; required): A list of the last step to ran in the context of this step. In the case of a DAG or a job this will be the last step that has been executed. It will remain empty for functions.
@,type,{Array<string>}
@,memberof,StepStatus
  - `outputs` (Array of Bool | Real | String | Dict | Arrays; required): The outputs produced by this step.
@,type,{Array<StepStringOutput | StepIntegerOutput | StepNumberOutput | StepBooleanOutput | StepFolderOutput | StepFileOutput | StepPathOutput | StepArrayOutput | StepJSONObjectOutput>}
@,memberof,StepStatus
  - `source` (String; optional): Source url for the status object. It can be a recipe or a function.
@,type,{string}
@,memberof,StepStatus
  - `started_at` (String; required): The time at which the task was started
@,type,{string}
@,memberof,StepStatus
  - `status` (a value equal to: 'Scheduled', 'Running', 'Failed', 'Succeeded', 'Skipped', 'Unknown'; optional): The status of this step.
@,type,{StepStatusEnum}
@,memberof,StepStatus
  - `status_type` (a value equal to: 'Function', 'DAG', 'Loop', 'Container', 'Unknown'; required): The type of step this status is for. Can be \"Function\", \"DAG\" or \"Loop\"
@,type,{StatusType}
@,memberof,StepStatus
  - `template_ref` (String; required): The name of the template that spawned this step
@,type,{string}
@,memberof,StepStatus
  - `type` (String; optional)
  - `type` (String; optional)
- `showOutput` (Bool; optional): Show inputs and outputs
- `showResult` (Bool; optional): Show visualization set of a CardFile directly
- `showStatusLabel` (Bool; optional): Show status label
"""
function ''_studyprogress(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath, :color, :isLocal, :projectName, :projectOwner, :refreshInterval, :run, :showOutput, :showResult, :showStatusLabel]
        wild_props = Symbol[]
        return Component("''_studyprogress", "StudyProgress", "pollination_dash_io", available_props, wild_props; kwargs...)
end

