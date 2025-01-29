function hydro = solveIRFs(hydro)
    hydro = radiationIRF_nopopup(hydro,20,[],[],[],[]);
    hydro = radiationIRFSS_nopopup(hydro,[],[]);
    hydro = excitationIRF_nopopup(hydro,20,[],[],[],[]);
end