# AUTO GENERATED FILE - DO NOT EDIT

export ''_managesettings

"""
    ''_managesettings(;kwargs...)

A ManageSettings component.
Use this component to get the host name
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `settings` (optional): Settings to apply. settings has the following type: lists containing elements 'location', 'units', 'layers', 'tolerance', 'angle_tolerance'.
Those elements have the following types:
  - `location` (required): . location has the following type: lists containing elements 'city', 'latitude', 'longitude', 'time_zone', 'elevation'.
Those elements have the following types:
  - `city` (String; required)
  - `latitude` (Real; required)
  - `longitude` (Real; required)
  - `time_zone` (Real; required)
  - `elevation` (Real; required)
  - `units` (a value equal to: 'Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters'; required)
  - `layers` (Array of Strings; required)
  - `tolerance` (Real; required)
  - `angle_tolerance` (Real; required)
"""
function ''_managesettings(; kwargs...)
        available_props = Symbol[:id, :settings]
        wild_props = Symbol[]
        return Component("''_managesettings", "ManageSettings", "pollination_dash_io", available_props, wild_props; kwargs...)
end

