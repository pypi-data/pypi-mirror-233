# AUTO GENERATED FILE - DO NOT EDIT

export ''_selectcloudartifact

"""
    ''_selectcloudartifact(;kwargs...)

A SelectCloudArtifact component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
- `fileNameMatch` (String; optional): File name filter
- `projectName` (String; optional): Name of the project
- `projectOwner` (String; optional): Owner of the project
- `studyId` (String; optional): ID of the job
- `value` (optional): Initial path where the files are. value has the following type: lists containing elements 'key'.
Those elements have the following types:
  - `key` (String; required)
"""
function ''_selectcloudartifact(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath, :fileNameMatch, :projectName, :projectOwner, :studyId, :value]
        wild_props = Symbol[]
        return Component("''_selectcloudartifact", "SelectCloudArtifact", "pollination_dash_io", available_props, wild_props; kwargs...)
end

