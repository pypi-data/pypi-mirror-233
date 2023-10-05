# AUTO GENERATED FILE - DO NOT EDIT

export ''_selectproject

"""
    ''_selectproject(;kwargs...)

A SelectProject component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
- `defaultProjectId` (String; optional): Default project
- `projectOwner` (String; optional): Owner of the project
"""
function ''_selectproject(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath, :defaultProjectId, :projectOwner]
        wild_props = Symbol[]
        return Component("''_selectproject", "SelectProject", "pollination_dash_io", available_props, wild_props; kwargs...)
end

