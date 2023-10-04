
module PollinationDashIo
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "1.0.0"

include("jl/''_authuser.jl")
include("jl/''_createstudy.jl")
include("jl/''_epwmap.jl")
include("jl/''_getgeometry.jl")
include("jl/''_gethbjson.jl")
include("jl/''_gethost.jl")
include("jl/''_managesettings.jl")
include("jl/''_readlocalfile.jl")
include("jl/''_recipeinputsform.jl")
include("jl/''_selectaccount.jl")
include("jl/''_selectcloudartifact.jl")
include("jl/''_selectproject.jl")
include("jl/''_selectrecipe.jl")
include("jl/''_selectrun.jl")
include("jl/''_selectstudy.jl")
include("jl/''_sendgeometry.jl")
include("jl/''_sendhbjson.jl")
include("jl/''_sendresults.jl")
include("jl/''_studyprogress.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "pollination_dash_io",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "pollination_dash_io.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "pollination_dash_io.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
