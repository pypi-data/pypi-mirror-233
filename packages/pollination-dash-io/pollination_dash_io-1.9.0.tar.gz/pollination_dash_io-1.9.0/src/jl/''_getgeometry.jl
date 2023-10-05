# AUTO GENERATED FILE - DO NOT EDIT

export ''_getgeometry

"""
    ''_getgeometry(;kwargs...)

A GetGeometry component.
Use this component to get geometry from CAD

State
- geometry (Array):
   Array of Ladybug Display Geometry
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `buttonLabel` (String; optional)
- `defaultKey` (String; required)
- `fullWidth` (Bool; optional)
- `geometryFilter` (optional): . geometryFilter has the following type: lists containing elements 'type', 'layer'.
Those elements have the following types:
  - `type` (Array of Strings; optional)
  - `layer` (Array of Strings; optional)
- `meshOptions` (optional): . meshOptions has the following type: lists containing elements 'gridSize', 'union'.
Those elements have the following types:
  - `gridSize` (Real; optional)
  - `union` (Bool; optional)
- `optionsConfig` (optional): . optionsConfig has the following type: lists containing elements 'selection', 'subscribe', 'preview'.
Those elements have the following types:
  - `selection` (required): . selection has the following type: lists containing elements 'show', 'selected'.
Those elements have the following types:
  - `show` (Bool; optional)
  - `selected` (Bool; optional)
  - `subscribe` (required): . subscribe has the following type: lists containing elements 'show', 'selected'.
Those elements have the following types:
  - `show` (Bool; optional)
  - `selected` (Bool; optional)
  - `preview` (required): . preview has the following type: lists containing elements 'show', 'selected'.
Those elements have the following types:
  - `show` (Bool; optional)
  - `selected` (Bool; optional)
- `useIcon` (Bool; optional)
"""
function ''_getgeometry(; kwargs...)
        available_props = Symbol[:id, :buttonLabel, :defaultKey, :fullWidth, :geometryFilter, :meshOptions, :optionsConfig, :useIcon]
        wild_props = Symbol[]
        return Component("''_getgeometry", "GetGeometry", "pollination_dash_io", available_props, wild_props; kwargs...)
end

