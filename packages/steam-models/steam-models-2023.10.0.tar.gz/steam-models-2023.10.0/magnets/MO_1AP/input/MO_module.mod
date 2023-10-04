-- include-file of the module from MO corrector magnet/Bernhard Auchmann
-- 01.09.00 - referring to: LHCMO_MC0002|2|A


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MO_RIN = 32.2;		mo_rin = MO_RIN*mm*mshrink;
MO_ROUT = 42.95;	mo_rout = MO_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmo1 = [beamd-mo_rout,0];
kpmo2 = [beamd+mo_rout,0];
kpmo3 = [beamd-mo_rin,0];
kpmo4 = [beamd+mo_rin,0];


-- LINES

lnmo1 = HyperLine(kpmo1,kpmo2,"Arc",mo_rout);
lnmo2 = HyperLine(kpmo3,kpmo4,"Arc",mo_rin);
lnmo3 = Line(kpmo1,kpmo3,0.54);
lnmo4 = Line(kpmo2,kpmo4,0.54);


-- AREAS

armo1 = HyperArea(lnmo1,lnmo3,lnmo2,lnmo4,BHiron2);


-- GRID-POINTS

Lmesh(lnmo1,40);
Lmesh(lnmo2,40);
Lmesh(lnmo3,4);
Lmesh(lnmo4,4);
