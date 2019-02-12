# Runbook

## Step 1. Download python client and install

```
git clone https://github.com/flexcompute/Flow360PythonClient.git flow360
cd flow360
pip3 install -r requirements.txt --user
```

## Step 2. Signing in with your account and password
```
python3
>>> import flow360
simulation.cloud email:********@gmail.com
Password: ***********
Do you want to keep logged in on this machine ([Y]es / [N]o)Y
```

## Step 3. Upload a mesh file
```
>>>flow360.newMesh(fname='flow360/tests/data/wing_tetra.1.lb8.ugrid', noSlipWalls=[1], meshName='my_experiment', tags=['wing'])
```
Replace above fname and noSlipWalls with your own file path and parameter.
Parameter inputs of mesh name and tags are optional.
Upon this command finishing, it will print the mesh Id '<mesh_id>'. Use that for next step.

## Step 4. Upload a case file
```
>>> flow360.newCase(meshId='<mesh_id>', config='flow360/tests/data/wing_tetra.1.json', caseName='case2', tags=['wing'])
```
Replace the mesh id generated from above step, and give your own config path.
Parameter inputs of caseName and tags are optional.
Upon this command finishing, it will print the case Id '<case_id>'. Use that for next step.

### Step 5. Checking the case status
```
>>> flow360.case.GetCaseInfo('<case_id>')
```
Look for field of "status" from printed result. A case status can be: 1) queued; 2) running; and 3) completed

## FAQ.

### How do I view a case result?
```
>>>flow360.case.DownloadCaseResults('<case_id>', '/tmp/result.tar.gz')
```
Replace the second parameter with your target location and output file name, ending with '.tar.gz'.

### My case is still running, but how can I check current residual or surface force result?
```
## this print out csv formated content
>>>flow360.case.GetCaseResidual('<case_id>') 
>>>flow360.case.GetCaseSurfaceForces('<case_id>', '<surface_id>')
```

### Where is my AWS credential stored locally?
Your AWS credential is encrypted and stored locally (if you hit Yes previously at authentication step) at
```
~/.flow360/
```
For security, your password is stored as hashed value, so nobody can guess your password.

### How to check my mesh processing status?


### How to check my case processing status?


### How can I download my mesh file?


### How can I download my case file?
