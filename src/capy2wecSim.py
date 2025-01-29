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

def capy2struct(hydro, dataset, V, cb, cg):
    # Naming Parameters
    hydro["body"] = dataset["body_name"].values
    hydro["body"] = 'flap'
    hydro["code"] = 'capytaine'
    hydro["file"] = dataset["body_name"].values
    hydro["file"] = 'flap'
    
	# Plot Parameters (convert to matlab.double for arrays)
    hydro["plotDofs"] = matlab.double(np.array([]))
    hydro["plotBodies"] = matlab.double(np.array([0.0]))
    hydro["plotDirections"] = matlab.double(np.array([0.0]))

    # Hydrodynamic Parameters
    hydro["dof"] = len(dataset["radiating_dof"].values)
    hydro["g"] = matlab.double(dataset["g"].values)
    hydro["rho"] = matlab.double(dataset["rho"].values)
    hydro["Nb"] = matlab.double([1])  # Single value should be passed as list/array to matlab

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
    hydro["K_hs"] = matlab.double(dataset["hydrostatic_stiffness"].values.tolist())
    hydro["Ainf"] = matlab.double(dataset['added_mass'].values[-1].tolist())

    # Radiation Results
    hydro["A"] = matlab.double(dataset['added_mass'].values[0:-1].tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["B"] = matlab.double(dataset['radiation_damping'].values[0:-1].tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])

    # Excitation, Froude-Krylov, and Diffraction Forces
    hydro["ex_re"] = matlab.double(np.real(dataset['excitation_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["ex_im"] = matlab.double(np.imag(dataset['excitation_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["ex_ma"] = matlab.double(np.abs(dataset['excitation_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["ex_ph"] = matlab.double(np.angle(dataset['excitation_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    
    hydro["fk_re"] = matlab.double(np.real(dataset['Froude_Krylov_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["fk_im"] = matlab.double(np.imag(dataset['Froude_Krylov_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["fk_ma"] = matlab.double(np.abs(dataset['Froude_Krylov_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["fk_ph"] = matlab.double(np.angle(dataset['Froude_Krylov_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    
    hydro["sc_re"] = matlab.double(np.real(dataset['diffraction_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["sc_im"] = matlab.double(np.imag(dataset['diffraction_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["sc_ma"] = matlab.double(np.abs(dataset['diffraction_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    hydro["sc_ph"] = matlab.double(np.angle(dataset['diffraction_force'].values[0:-1]).copy().tolist()).reshape(hydro["dof"],hydro["dof"],hydro["Nf"])
    return hydro