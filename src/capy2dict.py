import capytaine as capy
import numpy as np

def capy2dict(dataset,V,cb,cg):
	hydro = {}
	
	hydro["body"] = dataset["body_name"].values
	hydro["code"] = 'capytaine'
	hydro["file"] = dataset["body_name"].values

	hydro["plotDofs"] = np.array([])
	hydro["plotBodies"] = np.array([0])
	hydro["plotDirections"] = np.array([0])

	hydro["dof"] = dataset["radiating_dof"].values
	hydro["g"] = dataset["g"].values
	hydro["rho"] = dataset["rho"].values
	hydro["Nb"] = 1
	
	hydro["Nf"] = len(dataset["omega"].values)
	hydro["Nh"] = len(dataset["wave_direction"].values)
	hydro["w"] = dataset["omega"].values
	hydro["T"] = dataset["period"].values
	hydro["theta"] = dataset["wave_direction"].values

	hydro["Vo"] = V
	hydro["cb"] = cb
	hydro["cg"] = cg
	hydro["K_hs"] = dataset["hydrostatic_stiffness"].values
	hydro["Ainf"] = dataset['added_mass'].values[-1]

	hydro["A"] = dataset['added_mass'].values[0:-1]
	hydro["B"] = dataset['radiation_damping'].values[0:-1]
	
	hydro["ex_re"] = np.real(dataset['excitation_force'].values)
	hydro["ex_im"] = np.imag(dataset['excitation_force'].values)
	hydro["ex_ma"] = np.abs(dataset['excitation_force'].values)
	hydro["ex_ph"] = np.angle(dataset['excitation_force'].values)
	hydro["fk_re"] = np.real(dataset['Froude_Krylov_force'].values)
	hydro["fk_im"] = np.imag(dataset['Froude_Krylov_force'].values)
	hydro["fk_ma"] = np.abs(dataset['Froude_Krylov_force'].values)
	hydro["fk_ph"] = np.angle(dataset['Froude_Krylov_force'].values)
	hydro["sc_re"] = np.real(dataset['diffraction_force'].values)
	hydro["sc_im"] = np.imag(dataset['diffraction_force'].values)
	hydro["sc_ma"] = np.abs(dataset['diffraction_force'].values)
	hydro["sc_ph"] = np.angle(dataset['diffraction_force'].values)
	
	return hydro