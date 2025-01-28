import capytaine as capy
import numpy as np
import xarray as xr

def get_rectangle(w,t,h,draft,cog):
    mesh = capy.meshes.predefined.rectangles.mesh_parallelepiped(size=(t,w,h), resolution=(8,50,30), center=(0, 0, 0.5*h-draft),name='flap')
    body = capy.FloatingBody(mesh)
    body.keep_immersed_part()
    body.center_of_mass=np.array([0,0,cog])
    body.rotation_center = (0,0,-draft)
    body.add_rotation_dof(name='Pitch')
    body.keep_only_dofs(dofs='Pitch')
    print(body.mesh.nb_faces)
    #body.show_matplotlib()
    return body

def solve(body,omegas,beta,rho,depth):
    solver = capy.BEMSolver()
    hydrostatics =body.compute_hydrostatics()           # solves hydrostatics problem (no waves)
    #[S,D] = capy.Delhommeau().evaluate(body.mesh, body.mesh, free_surface=0.0, water_depth=depth, wavenumber=0.0)
    # Create problems and solve
    rad_prob = [capy.RadiationProblem(body=body,omega=omega,radiating_dof='Pitch', rho=rho, water_depth=depth) for omega in omegas]     # radiation
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    diff_prob = [capy.DiffractionProblem(body=body, wave_direction=beta, omega=omega, rho=rho, water_depth=depth) for omega in omegas]  # diffraction
    diff_result = solver.solve_all(diff_prob,keep_details=(True))

    # Infinite Frequency Radiation Problem
    inf_prob = capy.RadiationProblem(body=body, omega=np.inf, radiating_dof='Pitch', rho=rho, water_depth=depth)
    inf_result = solver.solve(inf_prob,keep_details=(True))

    # Assemble dataset
    dataset = capy.assemble_dataset(rad_result + diff_result + [inf_result])
    return dataset

def run(w,t,h,draft,cog,omegas,beta,rho,depth):
    body = get_rectangle(w,t,h,draft,cog)
    data = solve(body,omegas,beta,rho,depth)
    return data
