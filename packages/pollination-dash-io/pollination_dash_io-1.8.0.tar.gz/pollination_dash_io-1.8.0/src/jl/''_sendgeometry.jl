# AUTO GENERATED FILE - DO NOT EDIT

export ''_sendgeometry

"""
    ''_sendgeometry(;kwargs...)

A SendGeometry component.
Send geometry to a CAD Platform
geometry must be a single Display Geometry or Ladybug Geometry or a list of them
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `defaultAction` (a value equal to: 'add', 'delete', 'preview', 'clear', 'subscribe-preview'; optional)
- `defaultKey` (String; optional)
- `geometry` (Array of Strings; optional)
- `geometryOptions` (optional): . geometryOptions has the following type: lists containing elements 'units'.
Those elements have the following types:
  - `units` (a value equal to: 'Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters'; optional)
- `optionsConfig` (optional): . optionsConfig has the following type: lists containing elements 'add', 'delete', 'preview', 'clear', 'subscribe-preview'.
Those elements have the following types:
  - `add` (Bool; required)
  - `delete` (Bool; required)
  - `preview` (Bool; required)
  - `clear` (Bool; required)
  - `subscribe-preview` (Bool; required)
"""
function ''_sendgeometry(; kwargs...)
        available_props = Symbol[:id, :defaultAction, :defaultKey, :geometry, :geometryOptions, :optionsConfig]
        wild_props = Symbol[]
        return Component("''_sendgeometry", "SendGeometry", "pollination_dash_io", available_props, wild_props; kwargs...)
end

