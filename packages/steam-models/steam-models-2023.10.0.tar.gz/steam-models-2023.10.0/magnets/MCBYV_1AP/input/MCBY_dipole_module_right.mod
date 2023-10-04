-- include-file of the right dipole module from MCBY corrector magnet/Bernhard Auchmann
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

kpmcbyr1 = [beamd-mcby_rout,0];
kpmcbyr2 = [beamd+mcby_rout,0];
kpmcbyr3 = [beamd-mcby_rin,0];
kpmcbyr4 = [beamd+mcby_rin,0];
kpmcbyr5 = [beamd,mcby_rout];
kpmcbyr6 = [beamd,mcby_rin];


-- LINES

lnmcbyr2 = HyperLine(kpmcbyr1,kpmcbyr5,"Arc",mcby_rout);
lnmcbyr5 = HyperLine(kpmcbyr5,kpmcbyr2,"Arc",mcby_rout);
lnmcbyr1 = HyperLine(kpmcbyr3,kpmcbyr6,"Arc",mcby_rin);
lnmcbyr6 = HyperLine(kpmcbyr6,kpmcbyr4,"Arc",mcby_rin);
lnmcbyr3 = Line(kpmcbyr1,kpmcbyr3,0.54);
lnmcbyr4 = Line(kpmcbyr2,kpmcbyr4,0.54);
lnmcbyr7 = Line(kpmcbyr5,kpmcbyr6,0.54);


-- AREAS

armcbyr1 = HyperArea(lnmcbyr2,lnmcbyr3,lnmcbyr1,lnmcbyr7,BHiron2);
armcbyr2 = HyperArea(lnmcbyr7,lnmcbyr6,lnmcbyr4,lnmcbyr5,BHiron2);


-- GRID-POINTS

Lmesh(lnmcbyr1,20);
Lmesh(lnmcbyr2,20);
Lmesh(lnmcbyr3,5);
Lmesh(lnmcbyr4,5);
