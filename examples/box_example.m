% This code shows an example of how to use the code on a box geometry
clear;clc;close all;
setenv('PATH', [getenv('PATH'), ':~/NEMOH']);  	% Modify to add your installation of Nemoh to your path

addpath ../src
addpath ../src/geometries
% Create Directory for Output
projdir = 'exampleout';
if ~isfolder(projdir)
    % If it doesn't exist, create the directory
    mkdir(projdir);
end

% Build Geometry File
Length = 10;
Width = 20;
Draft = 5;
writegeominputfile_box(projdir,Length,Width,Draft,1);

% Build Mesh
target_nPanels = 300;
com = [0,0,-5];		% Center of Mass
writemeshcal(projdir,target_nPanels,com,1);
system(['mesh ',projdir]);

% Write Nemoh Input
water_depth = 600;
wavefreq = linspace(0.5,3,30);
wavedir = 0;
writenemohcal(projdir,wavefreq,wavedir,water_depth,1,com);

% Write Solver Inputs
writeinputsolvertxt(projdir,2,0.001,1,10,1e-5,1000)

% Pre-Processing 
system(['preProc ',projdir]);

% Hydrostatics
system(['hydrosCal ',projdir]);

% Solve
system(['solver ',projdir]);

% Post-Processing
system(['postProc ',projdir]);

% BEMIO
tic
disp('Now writing to h5...')
hydro = struct();
hydro = readNEMOH_nopopup(hydro,'exampleout');
hydro = radiationIRF_nopopup(hydro,20,[],[],[],[]);
hydro = radiationIRFSS_nopopup(hydro,[],[]);
hydro = excitationIRF_nopopup(hydro,20,[],[],[],[]);
for ii=1:hydro.Nb
	hydro.body{ii} = ['body',int2str(ii)];
end
writeBEMIOH5_nopopup(hydro)
toc
