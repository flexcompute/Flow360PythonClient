# Getting Started

## Step 1. Download python client and install
Make sure you have setuptools. If not, sudo apt-get install python3-setuptools
```
git clone https://github.com/flexcompute/Flow360PythonClient.git flow360
cd flow360
python3 setup.py install --user
```

## Step 2. Signing in with your account and password
An account can be created at www.flexcompute.com
```
python3
>>> import flow360client
simulation.cloud email:********@gmail.com
Password: ***********
Do you want to keep logged in on this machine ([Y]es / [N]o)Y
```

## Step 3. Upload a mesh file
First, specify a list of no-slip walls. If you have a .mapbc file, there is a function that will do this for you:
```
>>>noSlipWalls = flow360client.noSlipWallsFromMapbc('/path/to/meshname.mapbc')
```
Then submit a mesh
```
>>>meshId = flow360client.NewMesh(fname='flow360/tests/data/wing_tetra.1.lb8.ugrid', noSlipWalls=noSlipWalls, meshName='my_experiment', tags=['wing'])
```
Replace above fname and noSlipWalls with your own file path and parameter.
Parameter inputs of mesh name and tags are optional.
Upon this command finishing, it will return the mesh Id '<mesh_id>'. Use that for next step.

Note:
By default, submited mesh file will be processed using latest major release (e.g. 0.2.x) . If you want to run with another version of the solve, please specify in the argument as example:
```
>>>meshId = flow360client.NewMesh(fname='flow360/tests/data/wing_tetra.1.lb8.ugrid', noSlipWalls=noSlipWalls, meshName='my_experiment', tags=['wing'], solverVersion='release-0.2.1')
```

## Step 4. Upload a case file
First, prepare a JSON input file, either manually or by using the fun3d_to_flow360.py script:
```
python3 /path/to/flow360/flow360client/fun3d_to_flow360.py /path/to/fun3d.nml /path/to/mesh.mapbc /output/path/for/Flow360.json

```
Then submit a case:
```
>>> caseId = flow360client.NewCase(meshId='<mesh_id>', config='/output/path/for/Flow360.json', caseName='case2', tags=['wing'])
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
>>>flow360client.case.GetCaseSurfaceForces('<case_id>', '<surface_id>')
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
            "meshName" : "mesh.lb8.ugrid",  # not necessary
            "endianness" : "little", # not necessary
            "refArea" : 1.0, # Reference area, in grid units
            "momentCenter" : [0.0, 0.0, 0.0], # x,y,z moment center
            "momentLength" : [1.0, 1.0, 1.0] # x,y,z moment reference lengths
        },
        "runControl" :
        {
           "restart" : false, # restart not currently supported
           "maxSteps : 10000, # the maximum number of total steps, including parent case steps
           "firstOrderIterations" : -1, # number of iterations to perform before turning on second order accuracy
           "startControl" : -1 # Time step at which to start targetCL control. -1 is no trim control.
           "targetCL" : 0.0 # The desired trim CL to achieve
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
            "rotationCorrection" : false, # SARC model
            "DDES" : false # _true_ Enables DDES simulation
        },
        "freestream" :
        {
            "Reynolds" : 10000.0, # Reynolds number = Re_physical/ref_length_in_grid_units
            "Mach" : 0.3, # Mach number
            "Temperature" : 288.15, # Temperature in Kelvin
            "alphaAngle" : 0.0, # angle of attack
            "betaAngle" : 0.0 # side slip angle
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
        "initialCondition" : {
            "type" : "expression",         # options: "freestream" (default), "expression"
            "constants" : {                # all constants used to define the rho,u,v,w,p; optional for "type"=="expression"
                "a" : "sqrt(2)*pi*3^(-1/3)",
                "b" : "exp(2.5)+sin(2)"
            },
            "rho" : "cos(a*x)+sin(y)",           # required for "type"=="expression"
            "u" : "pow(x,2.5)+y/3",              # required for "type"=="expression"
            "v" : "a*sqrt(x)+pi*exp(pow(y,b))",  # required for "type"=="expression"
            "w" : "log(pi*a*x^2)",               # required for "type"=="expression"
            "p" : "log10(x/a)"                   # required for "type"=="expression"
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
* Re-start capability using a "parent" case. 

# Contact Support
* john@flexcompute.com
