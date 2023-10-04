-- include-file of the module from MCDO corrector magnet/Bernhard Auchmann
-- 01.09.00 - referring to: LHCMCDOA0001|0|A

-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MCDO_RIN  = 36.5;	mcdo_rin  = MCDO_RIN*mm*mshrink;
MCDO_ROUT = 47.6;	mcdo_rout = MCDO_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmcdo1 = [-mcdo_rout,0];
kpmcdo2 = [mcdo_rout,0];
kpmcdo3 = [-mcdo_rin,0];
kpmcdo4 = [mcdo_rin,0];
-- Per HAGEN
kpmcdo5 = [0,mcdo_rout];
kpmcdo6 = [0,mcdo_rin];


-- LINES

-- Per HAGEN
--lnmcdo1 = HyperLine(kpmcdo1,kpmcdo2,"Arc",mcdo_rout);
--lnmcdo2 = HyperLine(kpmcdo3,kpmcdo4,"Arc",mcdo_rin);
lnmcdo1 = HyperLine(kpmcdo1,kpmcdo2,"Arc",kpmcdo5);
lnmcdo2 = HyperLine(kpmcdo3,kpmcdo4,"Arc",kpmcdo6);
lnmcdo3 = Line(kpmcdo1,kpmcdo3,0.54);
lnmcdo4 = Line(kpmcdo2,kpmcdo4,0.54);


-- AREAS

armcdo1 = HyperArea(lnmcdo1,lnmcdo3,lnmcdo2,lnmcdo4,BHiron2);


-- GRID-POINTS

Lmesh(lnmcdo1,56);
Lmesh(lnmcdo2,56);
Lmesh(lnmcdo3,5);
Lmesh(lnmcdo4,5);
