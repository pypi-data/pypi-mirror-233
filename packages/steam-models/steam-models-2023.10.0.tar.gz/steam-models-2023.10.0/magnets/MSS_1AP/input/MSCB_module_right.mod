-- include-file of the right dipole and sextupole module from MSCB corrector magnet/Bernhard Auchmann
-- 29.08.00 - referring to: LHCMCBH_0001|0|A and LHCMS___0001|0|A

-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MSCB_RIN = 41.75;	mscb_rin = MSCB_RIN*mm*mshrink;
MSCB_ROUT = 79.9;	mscb_rout = MSCB_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- Keypoints

kpmscbr1 = [2*beamd-(beamd-mscb_rout),0];
kpmscbr2 = [2*beamd-(beamd+mscb_rout),0];
kpmscbr3 = [2*beamd-(beamd-mscb_rin),0];
kpmscbr4 = [2*beamd-(beamd+mscb_rin),0];
kpmscbr5 = [2*beamd-beamd,mscb_rout];
kpmscbr6 = [2*beamd-beamd,mscb_rin];

-- LINES

lnmscbr1 = HyperLine(kpmscbr2,kpmscbr5,"Arc",mscb_rout);
lnmscbr1b = HyperLine(kpmscbr5,kpmscbr1,"Arc",mscb_rout);
lnmscbr2 = HyperLine(kpmscbr4,kpmscbr6,"Arc",mscb_rin);
lnmscbr2b = HyperLine(kpmscbr6,kpmscbr3,"Arc",mscb_rin);
lnmscbr3 = Line(kpmscbr1,kpmscbr3,0.54);
lnmscbr4 = Line(kpmscbr2,kpmscbr4,0.54);
lnmscbr5 = Line(kpmscbr5,kpmscbr6,0.54);

-- AREAS

armscbr1 = HyperArea(lnmscbr4,lnmscbr2,lnmscbr5,lnmscbr1,BHiron2);
armscbr2 = HyperArea(lnmscbr3,lnmscbr1b,lnmscbr5,lnmscbr2b,BHiron2);

-- GRID-POINTS

Lmesh(lnmscbr1,18);
Lmesh(lnmscbr2,18);
Lmesh(lnmscbr1b,18);
Lmesh(lnmscbr2b,18);
Lmesh(lnmscbr3,8);
Lmesh(lnmscbr4,8);
Lmesh(lnmscbr5,8);
