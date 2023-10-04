-- include-file of the left dipole and sextupole module from MSCB corrector magnet/Bernhard Auchmann
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

kpmscbl1 = [-(beamd-mscb_rout),0];
kpmscbl2 = [-(beamd+mscb_rout),0];
kpmscbl3 = [-(beamd-mscb_rin),0];
kpmscbl4 = [-(beamd+mscb_rin),0];
kpmscbl5 = [-beamd,mscb_rout];
kpmscbl6 = [-beamd,mscb_rin];

-- LINES

lnmscbl1 = HyperLine(kpmscbl2,kpmscbl5,"Arc",mscb_rout);
lnmscbl1b = HyperLine(kpmscbl5,kpmscbl1,"Arc",mscb_rout);
lnmscbl2 = HyperLine(kpmscbl4,kpmscbl6,"Arc",mscb_rin);
lnmscbl2b = HyperLine(kpmscbl6,kpmscbl3,"Arc",mscb_rin);
lnmscbl3 = Line(kpmscbl1,kpmscbl3,0.54);
lnmscbl4 = Line(kpmscbl2,kpmscbl4,0.54);
lnmscbl5 = Line(kpmscbl5,kpmscbl6,0.54);

-- AREAS

armscbl1 = HyperArea(lnmscbl4,lnmscbl2,lnmscbl5,lnmscbl1,BHiron2);
armscbl2 = HyperArea(lnmscbl3,lnmscbl1b,lnmscbl5,lnmscbl2b,BHiron2);

-- GRID-POINTS

Lmesh(lnmscbl1,18);
Lmesh(lnmscbl2,18);
Lmesh(lnmscbl1b,18);
Lmesh(lnmscbl2b,18);
Lmesh(lnmscbl3,8);
Lmesh(lnmscbl4,8);
Lmesh(lnmscbl5,8);
