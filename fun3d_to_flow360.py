import sys
import json

try:
    fun3d_nml = open(sys.argv[1]).read()
    mapbc = open(sys.argv[2]).read()
except:
    print("Usage: python3 fun3d_to_flow360.py fun3d.nml CASE_NAME.mapbc")
    sys.exit(-1)

def process_nml(nml):
    groups = {}
    for line in nml.splitlines():
        line = line.strip()
        if '!' in line:
            line = line.split('!')[0].strip()

        if line == '':
            continue
        elif line.startswith('&'):
            group_key = line[1:]
            group = {}
        elif line == '/':
            groups[group_key] = group
            del group
            del group_key
        else:
            key, value = [a.strip() for a in line.split('=')]
            group[key.strip()] = value.strip()
    return groups

def translate_freestream(g):
    assert eval(g['temperature_units']) == 'Kelvin'
    return {
        'Mach' : float(g['mach_number']),
        'Reynolds' : float(g['reynolds_number']),
        'Temperature' : float(g['temperature']),
        'alphaAngle' : float(g['angle_of_attack']),
        'betaAngle' : float(g['angle_of_yaw'])
    }

def translate_geometry(g):
    return {
        "refArea" : float(g['area_reference']),
        "momentCenter" : [float(g['x_moment_center']),
                          float(g['y_moment_center']),
                          float(g['z_moment_center'])],
        "momentLength" : [float(g['x_moment_length']),
                          float(g['y_moment_length']),
                          float(g['z_moment_length'])]
    }

def translate_solver_params(g, **args):
    params = args
    args.update({
        "tolerance" : 1E-10,
        "linearIterations" : 30,
        "kappaMUSCL" : -1.0,
        "maxSteps" : int(g['steps']),
        "CFL" : {
            "initial" : 1.0,
            "final" : 100.0,
            "rampSteps" : 200
        }
    });
    return args

def translate_nml(nml):
    return {
        'freestream' :
            translate_freestream(nml['reference_physical_properties']),
        'geometry' :
            translate_geometry(nml['force_moment_integ_properties']),
        'navierStokesSolver' :
            translate_solver_params(nml['code_run_control']),
        'turbulenceModelSolver' :
            translate_solver_params(nml['code_run_control'],
                                    modelType='SpalartAllmaras'),
    }

def translate_boundaries(mapbc):
    mapbc = mapbc.strip().splitlines()
    num_bc = int(mapbc[0].strip())
    mapbc = mapbc[1:]
    assert len(mapbc) == num_bc
    bc = {}
    bc_map = {
        '4000': "NoSlipWall",
        '5000': "Freestream",
        '6662': "SlipWall"
    }
    noslipWalls = []
    for line in mapbc:
        bc_num, bc_type, bc_name = [i.strip() for i in line.split()]
        bc[bc_num] = {
            "type" : bc_map[bc_type],
            "name" : bc_name
        }
        if int(bc_type) == 4000:
            noslipWalls.append(int(bc_num))
    return bc, noslipWalls

bc, noslipWalls = translate_boundaries(mapbc)
print(str(noslipWalls))
nml = process_nml(fun3d_nml)
flow360_json = translate_nml(nml)
flow360_json['boundaries'] = bc
json.dump(flow360_json, sys.stdout, indent=4, sort_keys=True)
