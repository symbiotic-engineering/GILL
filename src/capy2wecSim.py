import capytaine as capy
import numpy as np
import matlab

def struct2dict(mat_struct):
    """Recursively converts a MATLAB struct to a Python dictionary."""
    py_dict = {}
    for key in mat_struct._fieldnames:
        value = getattr(mat_struct, key)
        if isinstance(value, matlab.mlarray.double):  # Convert MATLAB double arrays
            py_dict[key] = list(value)
        elif isinstance(value, matlab.struct):  # Recursively convert structs
            py_dict[key] = struct2dict(value)
        else:
            py_dict[key] = value
    return py_dict

def dict2struct(py_dict):
	"""Recursively converts a Python dictionary to a MATLAB struct."""
	mat_struct = matlab.struct()
	for key, value in py_dict.items():
		if isinstance(value, dict):  # Recursively convert nested dictionaries
			mat_struct[key] = dict2struct(value)
		elif isinstance(value, list):  # Convert lists to MATLAB double arrays
			mat_struct[key] = matlab.double(value)
		else:
			mat_struct[key] = value
	return mat_struct

'''def build_full_matrix(coef, dofs, Nf, omega_dependant = True):
    full_matrix = np.zeros((6,6,Nf))
    if 'Surge' in dofs:
        full_matrix[0,0,:] = coef[0,0,:]
        if 'Sway' in dofs:
            full_matrix[0,1,:] = coef[0,1,:]
            full_matrix[1,0,:] = coef[1,0,:]
            if 'Heave' in dofs:
                full_matrix[0,2,:] = coef[0,2,:]
                full_matrix[2,0,:] = coef[2,0,:]
                if 'Roll' in dofs:'''

def build_full_matrix(coef, dofs, Nf, omega_dependant=True, radiation=True):
    # Initialize the full matrix
    if omega_dependant:
        if radiation:
            full_matrix = np.zeros((6, 6, Nf))
        else:
            full_matrix = np.zeros((6, 1, Nf))
    else:
        if radiation:
            full_matrix = np.zeros((6, 6))
        else:
            full_matrix = np.zeros((6, 1))
    
    # Define mapping of DOFs to indices in the full_matrix
    dof_indices = {
        'Surge': 0,
        'Sway': 1,
        'Heave': 2,
        'Roll': 3,
        'Pitch': 4,
        'Yaw': 5
    }
    
    # Extract the indices for the given DOFs
    selected_indices = [dof_indices[dof] for dof in dofs]
    
    # Fill the full_matrix with values from coef
    for idx_ii, ii in enumerate(selected_indices):
        if radiation:
            for idx_jj, jj in enumerate(selected_indices):
                if omega_dependant:
                    full_matrix[ii, jj, :] = coef[idx_ii, idx_jj, :]
                else:
                    full_matrix[ii, jj] = coef[idx_ii, idx_jj]
        else:
            if omega_dependant:
                full_matrix[ii, 0, :] = coef[idx_ii, 0, :]
            else:
                full_matrix[ii, 0] = coef[idx_ii, 0]
    
    return full_matrix


def capy2struct(hydro, dataset, V, cb, cg):
    # Naming Parameters
    hydro["body"] = str(dataset["body_name"].values)
    hydro["code"] = 'CAPYTAINE'
    hydro["file"] = str(dataset["body_name"].values)
    
	# Plot Parameters (convert to matlab.double for arrays)
    hydro["plotDofs"] = matlab.double(np.array([]))
    hydro["plotBodies"] = matlab.double(np.array([0.0]))
    hydro["plotDirections"] = matlab.double(np.array([0.0]))

    # Hydrodynamic Parameters
    hydro["dof"] = len(dataset["radiating_dof"].values)
    hydro["g"] = matlab.double(dataset["g"].values)
    hydro["rho"] = matlab.double(dataset["rho"].values)
    hydro["Nb"] = matlab.double([1])  # Single value should be passed as list/array to matlab
    hydro["h"] = matlab.double(dataset["water_depth"].values)

    # Wave Parameters
    hydro["Nf"] = len(dataset["omega"].values)-1
    hydro["Nh"] = matlab.double([len(dataset["wave_direction"].values)])
    hydro["w"] = matlab.double(dataset["omega"].values[0:-1])
    hydro["T"] = matlab.double(dataset["period"].values[0:-1])
    hydro["theta"] = matlab.double(dataset["wave_direction"].values)

    # Basic Hydro Parameters
    hydro["Vo"] = matlab.double([V])  # If scalar, use list or array
    hydro["cb"] = matlab.double([cb])  # If scalar, use list or array
    hydro["cg"] = matlab.double([cg])  # If scalar, use list or array
    Khs = dataset["hydrostatic_stiffness"].values
    Khs = build_full_matrix(Khs, dataset["radiating_dof"].values, 0, omega_dependant=False)
    hydro["Khs"] = matlab.double(Khs.tolist())
    Ainf = dataset["added_mass"].values[-1]
    Ainf = build_full_matrix(Ainf, dataset["radiating_dof"].values, 0, omega_dependant=False)
    hydro["Ainf"] = matlab.double(Ainf.tolist())

    # Radiation Results
    A = dataset['added_mass'].values[0:-1].reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    A = build_full_matrix(A, dataset["radiating_dof"].values, hydro["Nf"])
    hydro["A"] = matlab.double(A.tolist())
    B = dataset['radiation_damping'].values[0:-1].reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    B = build_full_matrix(B, dataset["radiating_dof"].values, hydro["Nf"])
    hydro["B"] = matlab.double(B.tolist())

    # Excitation, Froude-Krylov, and Diffraction Forces
    exF = dataset['excitation_force'].values[0:-1].reshape(hydro["dof"],1,hydro["Nf"])
    exF = build_full_matrix(exF, dataset["influenced_dof"].values, hydro["Nf"], radiation=False)
    hydro["ex_re"] = matlab.double(np.real(exF).tolist())
    hydro["ex_im"] = matlab.double(np.imag(exF).tolist())
    hydro["ex_ma"] = matlab.double(np.abs(exF).tolist())
    hydro["ex_ph"] = matlab.double(np.angle(exF).tolist())
    
    fkF = dataset['Froude_Krylov_force'].values[0:-1].reshape(hydro["dof"],1,hydro["Nf"])
    fkF = build_full_matrix(fkF, dataset["influenced_dof"].values, hydro["Nf"], radiation=False)
    hydro["fk_re"] = matlab.double(np.real(fkF).tolist())
    hydro["fk_im"] = matlab.double(np.imag(fkF).tolist())
    hydro["fk_ma"] = matlab.double(np.abs(fkF).tolist())
    hydro["fk_ph"] = matlab.double(np.angle(fkF).tolist())

    scF = dataset['diffraction_force'].values[0:-1].reshape(hydro["dof"],1,hydro["Nf"])
    scF = build_full_matrix(scF, dataset["influenced_dof"].values, hydro["Nf"], radiation=False)
    hydro["sc_re"] = matlab.double(np.real(scF).tolist())
    hydro["sc_im"] = matlab.double(np.imag(scF).tolist())
    hydro["sc_ma"] = matlab.double(np.abs(scF).tolist())
    hydro["sc_ph"] = matlab.double(np.angle(scF).tolist())
    return hydro