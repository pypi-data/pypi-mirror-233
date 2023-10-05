# AUTO GENERATED FILE - DO NOT EDIT

export ''_selectrecipe

"""
    ''_selectrecipe(;kwargs...)

A SelectRecipe component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
- `projectName` (String; optional): Name of the project
- `projectOwner` (String; optional): Owner of the project
- `value` (optional): Default recipe filter. value has the following type: lists containing elements 'owner', 'name', 'tag'.
Those elements have the following types:
  - `owner` (String; required)
  - `name` (String; required)
  - `tag` (String; required)
"""
function ''_selectrecipe(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath, :projectName, :projectOwner, :value]
        wild_props = Symbol[]
        return Component("''_selectrecipe", "SelectRecipe", "pollination_dash_io", available_props, wild_props; kwargs...)
end

