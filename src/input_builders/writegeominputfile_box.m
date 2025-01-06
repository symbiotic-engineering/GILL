function [] = writegeominputfile_box(projdir,Length,Width,Draft,ii)
% Writes <geomInput-file>, the corse mesh, for box shaped body
% INPUTS:
%	projdir	->	[string]Directory where Nemoh related files are going
%	Length	->	[m]	Length of box
%	Width	->	[m]	Width of box
%	Draft	->	[m] 	Draft of box
%	ii	->	[#]	Body number
%
% OUTPUTS:
%	None, but builds <geomInput-file> named mesh#
%
% left face
X(1,:,:)=[-Length/2,0,-Draft;
	-Length/2,-Width/2,-Draft;
	-Length/2,-Width/2,0;
	-Length/2,0,0];
% Bottom face
X(2,:,:)=[-Length/2,-Width/2,-Draft;
	-Length/2,0,-Draft;
	Length/2,0,-Draft;
	Length/2,-Width/2,-Draft];
% right face
X(3,:,:)=[Length/2,0,-Draft;
	Length/2,0,0;
	Length/2,-Width/2,0;
	Length/2,-Width/2,-Draft];
% front face
X(4,:,:)=[-Length/2,-Width/2,-Draft;
	Length/2,-Width/2,-Draft;
	Length/2,-Width/2,0;
	-Length/2,-Width/2,0];

fid=fopen([projdir,filesep,'mesh',int2str(ii)],'w');
fprintf(fid,'%g \n',16);
fprintf(fid,'%g \n',4);
for jj=1:4
	for kk=1:4
            	x=X(jj,kk,1);
            	y=X(jj,kk,2);
            	z=X(jj,kk,3);
            	fprintf(fid,'%E %E %E \n',[x y z]);
        end
end
for jj=1:4
     	fprintf(fid,'%g %g %g %g \n',[4*(jj-1)+1 4*(jj-1)+2 4*(jj-1)+3 4*(jj-1)+4]');
end
status=fclose(fid);
