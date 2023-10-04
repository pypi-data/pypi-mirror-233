-- include-file of the right dipole module from MCBC corrector magnet/Bernhard Auchmann
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

kpmcbcr1 = [beamd-mcbc_rout,0];
kpmcbcr2 = [beamd+mcbc_rout,0];
kpmcbcr3 = [beamd-mcbc_rin,0];
kpmcbcr4 = [beamd+mcbc_rin,0];
kpmcbcr5 = [beamd,mcbc_rout];
kpmcbcr6 = [beamd,mcbc_rin];


-- LINES

lnmcbcr2 = HyperLine(kpmcbcr1,kpmcbcr5,"Arc",mcbc_rout);
lnmcbcr5 = HyperLine(kpmcbcr5,kpmcbcr2,"Arc",mcbc_rout);
lnmcbcr1 = HyperLine(kpmcbcr3,kpmcbcr6,"Arc",mcbc_rin);
lnmcbcr6 = HyperLine(kpmcbcr6,kpmcbcr4,"Arc",mcbc_rin);
lnmcbcr3 = Line(kpmcbcr1,kpmcbcr3,0.54);
lnmcbcr4 = Line(kpmcbcr2,kpmcbcr4,0.54);
lnmcbcr7 = Line(kpmcbcr5,kpmcbcr6,0.54);


-- AREAS

armcbcr1 = HyperArea(lnmcbcr2,lnmcbcr3,lnmcbcr1,lnmcbcr7,BHiron2);
armcbcr2 = HyperArea(lnmcbcr7,lnmcbcr6,lnmcbcr4,lnmcbcr5,BHiron2);


-- GRID-POINTS

Lmesh(lnmcbcr1,20);
Lmesh(lnmcbcr2,20);
Lmesh(lnmcbcr3,5);
Lmesh(lnmcbcr4,5);
