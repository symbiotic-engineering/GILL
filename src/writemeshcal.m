function [] = writemeshcal(projdir,target_nPanels,com,ii)
% Writes Mesh input file
% INPUTS:
%	projdir		->	[string]Directory where Nemoh related files are going
%	target_nPanels	->	[#]	Target number of panels for mesh
%	com		->	[m,m,m]	Centers of mass
%	ii		->	[#]	Body number
%
% OUTPUTS:
%	None, but builds Mesh.cal file in projdir
%
% Note that this does not allow for full utilization of all Nemoh features

fid=fopen([projdir,filesep,'Mesh.cal'],'w');  		
fprintf(fid,['mesh',int2str(ii),'\n']); 		% Name of geomInput-file, assumed mesh#
fprintf(fid,'1 \n %f 0. \n ',0);			% 1 for symmetry, + Translation???
fprintf(fid,'%f %f %f \n',com(ii,:));			% Center of Mass
fprintf(fid,'%g \n 2 \n 0. \n 1.\n',target_nPanels(ii));% target number of panels	
fprintf(fid,'%f \n',1025.);				% [kg/m^3] 	Density of seawater
fprintf(fid,'%f \n',9.81);				% [m/s^2]	Gravitiy Acceleration
status=fclose(fid);
end
