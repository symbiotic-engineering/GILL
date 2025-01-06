function [] = writenemohcal(projdir,wavefreq,wavedir,depth,nBodies,com)
% Writes Nemoh input file
% INPUTS:
%	projdir		->	[string]Directory where Nemoh related files are going
%	wavefreq	->	[rad/s]	List of Wave Frequecies
%	wavedir		->	[deg]	List of Wave Directions
%	depth		->	[m]	Water Depth
%	nBodies		->	[#]	Number of bodies
%	com		->	[m,m,m]	Centers of mass
%
% OUTPUTS:
%	None, but builds Nemoh.cal file in projdir
%
% Note that this does not allow for full utilization of all Nemoh features.

for ii=1:nBodies
	fid=fopen([projdir,filesep,'mesh',filesep,'mesh',int2str(ii),'.tec'],'r');
	line_read=fscanf(fid,'%s',2);
	nPoints(ii)=fscanf(fid,'%g',1);
	line_read=fscanf(fid,'%s',2);
	nPanels(ii)=fscanf(fid,'%g',1);
	status=fclose(fid);
end

fid=fopen([projdir,filesep,'Nemoh.cal'],'w');
fprintf(fid,'--- Environment ------------------------------------------------------------------------------------------------------------------ \n');
fprintf(fid,'1025.0				! RHO 			! KG/M**3 	! Fluid specific volume \n');
fprintf(fid,'9.81				! G			! M/S**2	! Gravity \n');
fprintf(fid,'%f                 ! DEPTH			! M		! Water depth\n',depth);
fprintf(fid,'0.	0.              ! XEFF YEFF		! M		! Wave measurement point\n');
fprintf(fid,'--- Description of floating bodies -----------------------------------------------------------------------------------------------\n');
fprintf(fid,'%g				! Number of bodies\n',nBodies);
for ii=1:nBodies
    fprintf(fid,'--- Body %g -----------------------------------------------------------------------------------------------------------------------\n',ii);
    fprintf(fid,['mesh',int2str(ii),'.dat\n']);
    fprintf(fid,'%g %g			! Number of points and number of panels 	\n',nPoints(ii),nPanels(ii));
    fprintf(fid,'6				! Number of degrees of freedom\n');
    fprintf(fid,'1 1. 0.	0. 0. 0. 0.		! Surge\n');
    fprintf(fid,'1 0. 1.	0. 0. 0. 0.		! Sway\n');
    fprintf(fid,'1 0. 0. 1. 0. 0. 0.		! Heave\n');
    fprintf(fid,'2 1. 0. 0. %f %f %f		! Roll about a point\n',com(ii,:));
    fprintf(fid,'2 0. 1. 0. %f %f %f		! Pitch about a point\n',com(ii,:));
    fprintf(fid,'2 0. 0. 1. %f %f %f		! Yaw about a point\n',com(ii,:));
    fprintf(fid,'6				! Number of resulting generalised forces\n');
    fprintf(fid,'1 1. 0.	0. 0. 0. 0.		! Force in x direction\n');
    fprintf(fid,'1 0. 1.	0. 0. 0. 0.		! Force in y direction\n');
    fprintf(fid,'1 0. 0. 1. 0. 0. 0.		! Force in z direction\n');
    fprintf(fid,'2 1. 0. 0. %f %f %f		! Moment force in x direction about a point\n',com(ii,:));
    fprintf(fid,'2 0. 1. 0. %f %f %f		! Moment force in y direction about a point\n',com(ii,:));
    fprintf(fid,'2 0. 0. 1. %f %f %f		! Moment force in z direction about a point\n',com(ii,:));
    fprintf(fid,'0				! Number of lines of additional information \n');
end
fprintf(fid,'--- Load cases to be solved -------------------------------------------------------------------------------------------------------\n');
fprintf(fid,'%g %g	%f	%f	! Freq type 1,2,3=[rad/s,Hz,s],Number of wave frequencies, Min, and Max (rad/s)\n',1,length(wavefreq),wavefreq(1),wavefreq(end));
fprintf(fid,'%g	%f	%f		! Number of wave directions, Min and Max (degrees)\n',length(wavedir),wavedir(1),wavedir(end));
fprintf(fid,'--- Post processing ---------------------------------------------------------------------------------------------------------------\n');
fprintf(fid,'0	0.1	10.         ! IRF 				! IRF calculation (0 for no calculation), time step and duration\n');
fprintf(fid,'0                  ! Show pressure\n');
fprintf(fid,'0	0.	180.		! Kochin function 		! Number of directions of calculation (0 for no calculations), Min and Max (degrees)\n');
fprintf(fid,'0	50	400. 400.   ! Free surface elevation 	! Number of points in x direction (0 for no calcutions) and y direction and dimensions of domain in x and y direction\n');
fprintf(fid,'0                  ! Response Amplitude Operator (RAO), 0 no calculation, 1 calculated\n');
fprintf(fid,'1					! output freq type, 1,2,3=[rad/s,Hz,s]\n');
fprintf(fid,'---QTF---\n');
fprintf(fid,'0         ! QTF flag, 1 is calculated \n');
fprintf(fid,'------\n');
status=fclose(fid);
fclose('all');
end
