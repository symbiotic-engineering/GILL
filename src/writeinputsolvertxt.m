function [] = writeinputsolvertxt(projdir,GQorder,epszmin,solver,restart,rel_tol,max_iter)
% Writes solver inputs file
% INPUTS:
%	projdir	->	[string]Directory where Nemoh related files are going
%	GQorder	->	[1-4] 	Gauss quadrature order N=[1,4] for surface integration, resulting in N^2 nodes
%	epszmin	->	[]	for determining minimum z of flow and source points of panel, zmin=epszmin*body_diameter
%	solver  ->	[0-2] 	Solver option: 0 for GAUSS ELIM., 1 for LU DECOMP., 2 for GMRES.
%	restart	->	[]	GMRES restart parameter, not needed for other solvers
%	rel_tol	->	[]	GMRES relative tolerance, not needed for other solvers
%	max_iter->	[]	GRMES maximum number of iterations, not needed for other solvers
%
% OUTPUTS:
%	None, but builds solver_input.txt file needed for Nemoh solver

fid=fopen([projdir,filesep,'input_solver.txt'],'w');
fprintf(fid,'%g				! Gauss quadrature (GQ) surface integration, N^2 GQ Nodes, specify N(1,4)\n',GQorder);
fprintf(fid,'%f			! eps_zmin for determine minimum z of flow and source points of panel, zmin=eps_zmin*body_diameter\n',epszmin);
fprintf(fid,'%g 				! 0 GAUSS ELIM.; 1 LU DECOMP.: 2 GMRES	!Linear system solver\n',solver);
fprintf(fid,'%g %f %g  	! Restart parameter, Relative Tolerance, max iter -> additional input for GMRES\n',restart,rel_tol,max_iter);
status=fclose(fid);
end
