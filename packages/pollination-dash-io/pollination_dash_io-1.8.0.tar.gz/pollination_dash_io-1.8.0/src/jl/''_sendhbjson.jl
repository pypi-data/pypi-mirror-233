# AUTO GENERATED FILE - DO NOT EDIT

export ''_sendhbjson

"""
    ''_sendhbjson(;kwargs...)

A SendHbjson component.
Send a HBJSON model to a CAD Platform
hbjson must be a valid HBJSON model
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `defaultAction` (a value equal to: 'add', 'delete', 'preview', 'clear', 'subscribe-preview', 'replace'; optional)
- `defaultKey` (String; optional)
- `hbjson` (Dict; optional)
- `optionsConfig` (optional): . optionsConfig has the following type: lists containing elements 'add', 'delete', 'preview', 'clear', 'subscribe-preview', 'replace'.
Those elements have the following types:
  - `add` (Bool; required)
  - `delete` (Bool; required)
  - `preview` (Bool; required)
  - `clear` (Bool; required)
  - `subscribe-preview` (Bool; required)
  - `replace` (Bool; required)
"""
function ''_sendhbjson(; kwargs...)
        available_props = Symbol[:id, :defaultAction, :defaultKey, :hbjson, :optionsConfig]
        wild_props = Symbol[]
        return Component("''_sendhbjson", "SendHbjson", "pollination_dash_io", available_props, wild_props; kwargs...)
end

