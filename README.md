# Getting Started

## Step 1. install flow360 client
Make sure you have setuptools. If not, sudo apt-get install python3-setuptools
```
pip3 install flow360client
```

## Step 2. Signing in with your account and password
An account can be created at www.flexcompute.com
```
python3
>>> import flow360client
enter your email registered at flexcompute:********@gmail.com
Password: ***********
Do you want to keep logged in on this machine ([Y]es / [N]o)Y
```

## Step 3. Upload a mesh file
A mesh of the ONERA M6 wing can be downloaded [here](https://flow360public.s3-us-west-1.amazonaws.com/wing_tetra.1.lb8.ugrid).

First, specify a list of no-slip walls. If you have a .mapbc file, there is a function that will do this for you:
```
>>>noSlipWalls = flow360client.noSlipWallsFromMapbc('/path/to/meshname.mapbc')
```
For the above example mesh of ONERA M6 wing, the surface ID of the wing is 1, so you can set noSlipWalls:
```
>>>noSlipWalls = [1]
```
If there are multiple surfaces of no-slip walls in your mesh, use a comma between them, e.g. noSlipWalls=[1,3,7]

Then submit a mesh
```
>>>meshId = flow360client.NewMesh(fname='flow360/tests/data/wing_tetra.1.lb8.ugrid', noSlipWalls=noSlipWalls, meshName='my_experiment', tags=['wing'])
>>>meshId = flow360client.NewMesh(fname='flow360/tests/data/wing_tetra.1.lb8.ugrid', meshJson=meshJsonObject, meshName='my_experiment', tags=['wing'])

```
Replace above fname and noSlipWalls with your own file path and parameter. Currently the only supported format is UGRID. Allowable extensions are .ugrid, .ugrid.gz, and .ugrid.bz2. 
Parameter inputs of mesh name and tags are optional.
Upon this command finishing, it will return the mesh Id '<mesh_id>'. Use that for next step.

Note:
By default, submited mesh file will be processed using latest major release (e.g. 0.2.x) . If you want to run with another version of the solve, please specify in the argument as example:
```
>>>meshId = flow360client.NewMesh(fname='flow360/tests/data/wing_tetra.1.lb8.ugrid', noSlipWalls=noSlipWalls, meshName='my_experiment', tags=['onera_wing'], solverVersion='release-0.2.1')
```

## Step 4. Upload a case file
First, prepare a JSON input file, either manually or by using the fun3d_to_flow360.py script:
```
python3 /path/to/flow360/flow360client/fun3d_to_flow360.py /path/to/fun3d.nml /path/to/mesh.mapbc /output/path/for/Flow360.json

```
A JSON file corresponding to the ONERA M6 wing test case can be found [here](https://flow360public.s3-us-west-1.amazonaws.com/Flow360_onera.json).

Then submit a case:
```
>>> caseId = flow360client.NewCase(meshId='<mesh_id>', config='/path/to/Flow360.json', caseName='case2', tags=['wing'])
```
Replace the mesh id generated from above step, and give your own config path.
Parameter inputs of caseName and tags are optional.
Upon this command finishing, it will return the case Id '<case_id>'. Use that for next step.

### Step 5. Checking the case status
```
>>> flow360client.case.GetCaseInfo('<case_id>')
```
Look for field of "status" from printed result. A case status can be: 1) queued; 2) running; and 3) completed

## FAQ.

### How do I download or view a finished case result?
To download the surface data (surface distributions and slices):
```
>>>flow360client.case.DownloadSurfaceResults('<case_id>', '/tmp/surfaces.tar.gz')
```
Replace the second parameter with your target location and output file name, ending with '.tar.gz'.

To download the entire flowfield:
```
>>>flow360client.case.DownloadVolumetricResults('<case_id>', '/tmp/volume.tar.gz')
```

### My case is still running, but how can I check current residual or surface force result?
```
## this print out csv formated content
>>>flow360client.case.GetCaseResidual('<case_id>') 
>>>flow360client.case.GetCaseSurfaceForces('<case_id>', [{'surfaceName' : <surface_name0>, 'surfaceIds' : [<id0>, <id1>, ...]}])
```

### Where is my AWS credential stored locally?
Your AWS credential is encrypted and stored locally (if you hit Yes previously at authentication step) at
```
~/.flow360/
```
For security, your password is stored as hashed value, so nobody can guess your password.

### How to check my mesh processing status?
```
## to list all your mesh files
>>> flow360client.mesh.ListMeshes()
## to view one particular mesh
>>> flow360client.mesh.GetMeshInfo('<mesh_id>')
```

### How can I delete my mesh or case?
```
## Delete a mesh
>>>flow360client.mesh.DeleteMesh('<mesh_id>')
## Delete a case
>>> flow360client.case.DeleteCase('<case_id>')
```
Caution: You won't be able to recover your deleted case or mesh files including its results after your deletion.

# Current Solver Input Options and Default Values
Caution: comments are not allowed to be submitted with the solver input.

    {
        "geometry" :
        {
            "refArea" : 1.0, # Reference area, in grid units
            "momentCenter" : [0.0, 0.0, 0.0], # x,y,z moment center
            "momentLength" : [1.0, 1.0, 1.0] # x,y,z moment reference lengths
        },
        "freestream" :
        {
            "Reynolds" : 10000.0, # REQUIRED. Reynolds number = Re_physical/ref_length_in_grid_units
            "Mach" : 0.3, # REQUIRED. Mach number
            "Temperature" : 288.15, # REQUIRED Temperature in Kelvin
            "alphaAngle" : 0.0, # REQUIRED. angle of attack
            "betaAngle" : 0.0 # REQUIRED. side slip angle
        },
        "runControl" :
        {
           "firstOrderIterations" : -1, # number of iterations to perform before turning on second order accuracy
           "startControl" : -1, # Time step at which to start targetCL control. -1 is no trim control.
           "targetCL" : 0.0 ,# The desired trim CL to achieve,
           "maxSteps" : 10000 # the maximum number of time steps or iterations to take
        },
        "boundaries" :
        {
            # List of boundary conditions. e.g.
            "1" : {
                "type" : "NoSlipWall"
            },
            "2" : {
                "type" : "SlipWall"
            },
            "3" : {
                "type" : "Freestream"
            }
        },
        "volumeOutput" : {
            "outputFormat" : "paraview", # "paraview" || "tecplot"
            "primitiveVars" : true, # outputs rho, u, v, w, p
            "vorticity" : false, # vorticity
            "residualNavierStokes" : false, # 5 components of the N-S residual
            "residualTurbulence" : false, # nuHat
            "T" : false, # Temperature
            "s" : false, # entropy
            "Cp" : true, # Coefficient of pressure
            "mut" : true, # turbulent viscosity
            "mutRatio" : false, # mut/mu_inf
            "Mach" : true # Mach number
        },
        "surfaceOutput" : {
            "outputFormat" : "paraview", # "paraview" || "tecplot"
            "primitiveVars" : true, # rho, u, v, w, p
            "Cp" : true, # Coefficient of pressure
            "Cf" : true, # Skin friction coefficient
            "CfVec" : true, # Viscous stress coefficient vector
            "yPlus" : true, # y+
            "wallDistance" : false, # wall Distance
            "Mach" : false # Mach number
        },
        "sliceOutput" : {        
            "outputFormat" : "paraview", # "paraview" || "tecplot"
            "primitiveVars" : true, # outputs rho, u, v, w, p
            "vorticity" : false, # vorticity
            "T" : false, # Temperature
            "s" : false, # entropy
            "Cp" : true, # Coefficient of pressure
            "mut" : true, # turbulent viscosity
            "mutRatio" : false, # mut/mu_inf
            "Mach" : true, # Mach number
            "slices" : [  # list of slices to save after the solver has finished
              {                  
                "sliceName" : "slice_1", # Name of the first slice
                "sliceNormal" : [0.0, 1.0, 0.0], # Normal vector of the first slice
                "sliceOrigin" : [0.0, 0.0, 0.0] # Origin of the first slice
              }
            ]                 
        },
        "navierStokesSolver" : {
            "tolerance" : 1e-10, # Tolerance for the NS residual, below which the solver exits
            "CFL": { # Exponential CFL ramping, from initial to final, over _rampSteps_ steps
                "initial" : 10.0,
                "final" : 200.0,
                "rampSteps" : 200
            },
            "linearIterations" : 25, # Number of iterations for the linear solver to perform
            "kappaMUSCL" : 0.3333333333333 # kappa for the MUSCL scheme, range from [-1, 1], with 1 being unstable.
            "maxDt" : 1.0e100, # Maximum time step
            "startEnforcingMaxDtStep" : -1, # time step at which to start enforcing maxDtStep. Default of -1 does not enforce a max time step.
            "updateJacobianFrequency" : 4, # Frequency at which the jacobian is updated.
            "equationEvalFrequency" : 1, # Frequency at which to update the NS equation in loosely-coupled simulations
            "viscousWaveSpeedScale" : 0.0 # Scales the wave speed acording to a viscous flux. 0.0 is no speed correction, with larger values providing a larger viscous wave speed correction.
        },
        "turbulenceModelSolver" : {
           "modelType" : "SpalartAllmaras", # Only SA supported at this point
            "CFL" : { # Exponential CFL ramping, from initial to final, over _rampSteps_ steps
                "initial" : 10,
                "final" : 200,
                "rampSteps" : 200
            },
            "linearIterations" : 15, # Number of linear iterations for the SA linear system
            "kappaMUSCL" : -1.0, # kappa for the muscle scheme, range from [-1, 1] with 1 being unstable.
            "updateJacobianFrequency" : 4, # frequency at which to update the Jacobian
            "equationEvalFrequency" : 4, # frequency at which to evaluate the turbulence equation in loosely-coupled simulations
            "rotationCorrection" : false, # SARC model
            "DDES" : false # _true_ Enables DDES simulation
        }
    }

# Version history
Results between major versions (e.g. x.y.0) may differ slightly. However, results among minor versions (e.g. 0.2.x) will not change.

## release-0.1
* Viscous gradient scheme changed from node-based Green-Gauss gradients to a Least-squares gradient scheme
* Improved both pressure and velocity limiters to help with supersonic and transonic cases.

## release-0.2.0
* Minor modifications to enhance convergence

## release-0.2.1
* Added support for tecplot .szplt output
* Added support for slicing of the final flowfield

## release-0.3.0
* Implemented incremental back-off in solution update
* Replaced the pressure/density limiters which were edge-based with node-based limiters.
* Improved the stability properties of the solution gradient used for the viscous fluxes. 
* Now using a blending of corrected and uncorrected viscous scheme. This effectively limits how much the corrected viscous scheme can differ from the uncorrected scheme. This is necessary because the Jacobian only includes contributions from the uncorrected scheme. 
* Bug fix for supersonic farfield boundary condition. 
* Tecplot output and single-file surface and slice output

# Contact Support
* john@flexcompute.com
