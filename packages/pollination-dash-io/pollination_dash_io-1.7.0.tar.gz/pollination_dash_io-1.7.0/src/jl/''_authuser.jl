# AUTO GENERATED FILE - DO NOT EDIT

export ''_authuser

"""
    ''_authuser(;kwargs...)

An AuthUser component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accessToken` (String; optional): JWT token
- `apiKey` (String; optional): API key from Pollination Cloud
- `basePath` (String; optional): Base path of the API.
"""
function ''_authuser(; kwargs...)
        available_props = Symbol[:id, :accessToken, :apiKey, :basePath]
        wild_props = Symbol[]
        return Component("''_authuser", "AuthUser", "pollination_dash_io", available_props, wild_props; kwargs...)
end

