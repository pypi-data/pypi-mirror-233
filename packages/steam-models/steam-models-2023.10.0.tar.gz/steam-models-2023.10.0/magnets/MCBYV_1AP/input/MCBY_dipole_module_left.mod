-- include-file of the left dipole module from MCBY corrector magnet/Bernhard Auchmann
-- 29.08.00 - referring to: LHCMCBYM0001|0


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *

MCBY_RIN = 48.15;	mcby_rin = MCBY_RIN*mm*mshrink;
MCBY_ROUT = 79.9;	mcby_rout = MCBY_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmcbyl1 = [-(beamd-mcby_rout),0];
kpmcbyl2 = [-(beamd+mcby_rout),0];
kpmcbyl3 = [-(beamd-mcby_rin),0];
kpmcbyl4 = [-(beamd+mcby_rin),0];
kpmcbyl5 = [-beamd,mcby_rout];
kpmcbyl6 = [-beamd,mcby_rin];


-- LINES

lnmcbyl2 = HyperLine(kpmcbyl5,kpmcbyl1,"Arc",mcby_rout);
lnmcbyl5 = HyperLine(kpmcbyl2,kpmcbyl5,"Arc",mcby_rout);
lnmcbyl1 = HyperLine(kpmcbyl6,kpmcbyl3,"Arc",mcby_rin);
lnmcbyl6 = HyperLine(kpmcbyl4,kpmcbyl6,"Arc",mcby_rin);
lnmcbyl3 = Line(kpmcbyl1,kpmcbyl3,0.54);
lnmcbyl4 = Line(kpmcbyl2,kpmcbyl4,0.54);
lnmcbyl7 = Line(kpmcbyl5,kpmcbyl6,0.54);


-- AREAS

armcbyl1 = HyperArea(lnmcbyl7,lnmcbyl1,lnmcbyl3,lnmcbyl2,BHiron2);
armcbyl2 = HyperArea(lnmcbyl4,lnmcbyl6,lnmcbyl7,lnmcbyl5,BHiron2);


-- GRID-POINTS

Lmesh(lnmcbyl1,20);
Lmesh(lnmcbyl2,20);
Lmesh(lnmcbyl3,5);
Lmesh(lnmcbyl4,5);

