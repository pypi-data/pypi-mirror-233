# AUTO GENERATED FILE - DO NOT EDIT

export ''_createstudy

"""
    ''_createstudy(;kwargs...)

A CreateStudy component.
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
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
"""
function ''_createstudy(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath]
        wild_props = Symbol[]
        return Component("''_createstudy", "CreateStudy", "pollination_dash_io", available_props, wild_props; kwargs...)
end

