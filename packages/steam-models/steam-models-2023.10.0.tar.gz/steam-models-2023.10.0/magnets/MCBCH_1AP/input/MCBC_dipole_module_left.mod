-- include-file of the left dipole module from MCBC corrector magnet/Bernhard Auchmann
-- 29.08.00 - referring to: LHCMCBCM0001|0


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *

MCBC_RIN = 40.5;	mcbc_rin = MCBC_RIN*mm*mshrink;
MCBC_ROUT = 79.9;	mcbc_rout = MCBC_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmcbcl1 = [-(beamd-mcbc_rout),0];
kpmcbcl2 = [-(beamd+mcbc_rout),0];
kpmcbcl3 = [-(beamd-mcbc_rin),0];
kpmcbcl4 = [-(beamd+mcbc_rin),0];
kpmcbcl5 = [-beamd,mcbc_rout];
kpmcbcl6 = [-beamd,mcbc_rin];


-- LINES

lnmcbcl2 = HyperLine(kpmcbcl5,kpmcbcl1,"Arc",mcbc_rout);
lnmcbcl5 = HyperLine(kpmcbcl2,kpmcbcl5,"Arc",mcbc_rout);
lnmcbcl1 = HyperLine(kpmcbcl6,kpmcbcl3,"Arc",mcbc_rin);
lnmcbcl6 = HyperLine(kpmcbcl4,kpmcbcl6,"Arc",mcbc_rin);
lnmcbcl3 = Line(kpmcbcl1,kpmcbcl3,0.54);
lnmcbcl4 = Line(kpmcbcl2,kpmcbcl4,0.54);
lnmcbcl7 = Line(kpmcbcl5,kpmcbcl6,0.54);


-- AREAS

armcbcl1 = HyperArea(lnmcbcl7,lnmcbcl1,lnmcbcl3,lnmcbcl2,BHiron2);
armcbcl2 = HyperArea(lnmcbcl4,lnmcbcl6,lnmcbcl7,lnmcbcl5,BHiron2);


-- GRID-POINTS

Lmesh(lnmcbcl1,20);
Lmesh(lnmcbcl2,20);
Lmesh(lnmcbcl3,5);
Lmesh(lnmcbcl4,5);
