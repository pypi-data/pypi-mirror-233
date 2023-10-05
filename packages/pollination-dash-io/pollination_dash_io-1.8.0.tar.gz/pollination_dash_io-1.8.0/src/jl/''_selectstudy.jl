# AUTO GENERATED FILE - DO NOT EDIT

export ''_selectstudy

"""
    ''_selectstudy(;kwargs...)

A SelectStudy component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
- `projectName` (String; optional): Name of the project
- `projectOwner` (String; optional): Owner of the project
- `studyId` (String; optional): Default ID of the study
- `value` (optional): Default cloud job. value has the following type: lists containing elements 'author', 'id', 'owner', 'recipe', 'resources_duration', 'spec', 'status'.
Those elements have the following types:
  - `author` (optional): author
@,type,{AccountPublic}
@,memberof,CloudJob. author has the following type: lists containing elements 'account_type', 'description', 'display_name', 'id', 'name', 'picture_url'.
Those elements have the following types:
  - `account_type` (String; required)
  - `description` (String; optional)
  - `display_name` (String; optional)
  - `id` (String; required)
  - `name` (String; required)
  - `picture_url` (String; optional): https://robohash.org/ladybugbot
@,type,{string}
@,memberof,AccountPublic
  - `id` (String; required): The unique ID for this run
@,type,{string}
@,memberof,CloudJob
  - `owner` (optional): owner
@,type,{AccountPublic}
@,memberof,CloudJob. owner has the following type: lists containing elements 'account_type', 'description', 'display_name', 'id', 'name', 'picture_url'.
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
@,memberof,CloudJob. recipe has the following type: lists containing elements 'annotations', 'api_version', 'inputs', 'metadata', 'outputs', 'source', 'type'.
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
  - `resources_duration` (optional): CPU and Memory usage aggregated for all runs in this job
@,type,{ResourcesDuration}
@,memberof,CloudJob. resources_duration has the following type: lists containing elements 'cpu', 'memory'.
Those elements have the following types:
  - `cpu` (Real; optional)
  - `memory` (Real; optional)
  - `spec` (required): The job specification
@,type,{Job}
@,memberof,CloudJob. spec has the following type: lists containing elements 'annotations', 'api_version', 'arguments', 'description', 'labels', 'name', 'source', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,Job
  - `api_version` (String; optional)
  - `arguments` (Array of Array of Bool | Real | String | Dict | Arrayss; optional): Input arguments for this job.
@,type,{Array<Array<JobArgument | JobPathArgument>>}
@,memberof,Job
  - `description` (String; optional): Run description.
@,type,{string}
@,memberof,Job
  - `labels` (Dict with Strings as keys and values of type String; optional): Optional user data as a dictionary. User data is for user reference only and will not be used in the execution of the job.
@,type,{{ [key: string]: string; }}
@,memberof,Job
  - `name` (String; optional): An optional name for this job. This name will be used a the display name for the run.
@,type,{string}
@,memberof,Job
  - `source` (String; required): The source url for downloading the recipe.
@,type,{string}
@,memberof,Job
  - `type` (String; optional)
  - `status` (optional): The status of the job
@,type,{JobStatus}
@,memberof,CloudJob. status has the following type: lists containing elements 'annotations', 'api_version', 'finished_at', 'id', 'message', 'runs_cancelled', 'runs_completed', 'runs_failed', 'runs_pending', 'runs_running', 'source', 'started_at', 'status', 'type'.
Those elements have the following types:
  - `annotations` (Dict with Strings as keys and values of type String; optional): An optional dictionary to add annotations to inputs. These annotations will be used by the client side libraries.
@,type,{{ [key: string]: string; }}
@,memberof,JobStatus
  - `api_version` (String; optional)
  - `finished_at` (String; optional): The time at which the task was completed
@,type,{string}
@,memberof,JobStatus
  - `id` (String; required): The ID of the individual job.
@,type,{string}
@,memberof,JobStatus
  - `message` (String; optional): Any message produced by the job. Usually error/debugging hints.
@,type,{string}
@,memberof,JobStatus
  - `runs_cancelled` (Real; optional): The count of runs that have been cancelled
@,type,{number}
@,memberof,JobStatus
  - `runs_completed` (Real; optional): The count of runs that have completed
@,type,{number}
@,memberof,JobStatus
  - `runs_failed` (Real; optional): The count of runs that have failed
@,type,{number}
@,memberof,JobStatus
  - `runs_pending` (Real; optional): The count of runs that are pending
@,type,{number}
@,memberof,JobStatus
  - `runs_running` (Real; optional): The count of runs that are running
@,type,{number}
@,memberof,JobStatus
  - `source` (String; optional): Source url for the status object. It can be a recipe or a function.
@,type,{string}
@,memberof,JobStatus
  - `started_at` (String; required): The time at which the job was started
@,type,{string}
@,memberof,JobStatus
  - `status` (a value equal to: 'Created', 'Pre-Processing', 'Running', 'Failed', 'Cancelled', 'Completed', 'Unknown'; optional): The status of this job.
@,type,{JobStatusEnum}
@,memberof,JobStatus
  - `type` (String; optional)
"""
function ''_selectstudy(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath, :projectName, :projectOwner, :studyId, :value]
        wild_props = Symbol[]
        return Component("''_selectstudy", "SelectStudy", "pollination_dash_io", available_props, wild_props; kwargs...)
end

