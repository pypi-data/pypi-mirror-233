# AUTO GENERATED FILE - DO NOT EDIT

export ''_selectaccount

"""
    ''_selectaccount(;kwargs...)

A SelectAccount component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
- `defaultAccountName` (String; optional): Default account name
"""
function ''_selectaccount(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath, :defaultAccountName]
        wild_props = Symbol[]
        return Component("''_selectaccount", "SelectAccount", "pollination_dash_io", available_props, wild_props; kwargs...)
end

