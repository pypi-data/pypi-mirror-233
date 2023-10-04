# AUTO GENERATED FILE - DO NOT EDIT

export ''_gethost

"""
    ''_gethost(;kwargs...)

A GetHost component.
Use this component to get the host name

State
- host (string):
   Name of the host
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
"""
function ''_gethost(; kwargs...)
        available_props = Symbol[:id]
        wild_props = Symbol[]
        return Component("''_gethost", "GetHost", "pollination_dash_io", available_props, wild_props; kwargs...)
end

