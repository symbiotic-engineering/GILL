# GILL
Used to communicate between Nemoh and WEC-Sim. Requires both Nemoh and WEC-Sim for effective use. Right now can only make boxes, but could be modified to accommodate other shapes.

Nate - njd76@cornell.edu

MIT License

The src folder contains all required scripts. The "write" scripts create the necessary input files for NEMOH. The scripts ending in nopopup are rewrites of some WEC-Sim code that had built in popups, the popups make them unable to run in -nojvm mode. The subfolder in src named geometries contains the write scripts for different geometry input files. Currently, there is only a box, but if you'd like to contribute I'd be happy to add others, or you can make your own elsewhere. 

The examples folder shows how to use the code. You can run the example code by typing run examples/box_example into a MATLAB command window.
