# Runbook

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
```
>>>flow360client.case.DownloadCaseResults('<case_id>', '/tmp/result.tar.gz')
```
Replace the second parameter with your target location and output file name, ending with '.tar.gz'.

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
