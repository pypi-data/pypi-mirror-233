# AUTO GENERATED FILE - DO NOT EDIT

export ''_readlocalfile

"""
    ''_readlocalfile(;kwargs...)

A ReadLocalFile component.
Use this component to get user info
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `filePath` (String; required): Full path or relative path where the file is
"""
function ''_readlocalfile(; kwargs...)
        available_props = Symbol[:id, :filePath]
        wild_props = Symbol[]
        return Component("''_readlocalfile", "ReadLocalFile", "pollination_dash_io", available_props, wild_props; kwargs...)
end

