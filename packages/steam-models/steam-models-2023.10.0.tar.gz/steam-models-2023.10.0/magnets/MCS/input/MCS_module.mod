-- include-file of the module from MCS corrector magnet/Bernhard Auchmann
-- 01.09.00 - referring to: LHCMCSMG0002|1|A


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MCS_RIN  = 33.5;	mcs_rin  = MCS_RIN*mm*mshrink;
MCS_ROUT = 44.95;	mcs_rout = MCS_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmcs1 = [-mcs_rout,0];
kpmcs2 = [mcs_rout,0];
kpmcs3 = [-mcs_rin,0];
kpmcs4 = [mcs_rin,0];
-- Per HAGEN
kpmcs5 = [0,mcs_rout];
kpmcs6 = [0,mcs_rin];


-- LINES

-- Per HAGEN
--lnmcs1 = HyperLine(kpmcs1,kpmcs2,"Arc",mcs_rout);
lnmcs1 = HyperLine(kpmcs1,kpmcs2,"Arc",kpmcs5);
--lnmcs2 = HyperLine(kpmcs3,kpmcs4,"Arc",mcs_rin);
lnmcs2 = HyperLine(kpmcs3,kpmcs4,"Arc",kpmcs6);
lnmcs3 = Line(kpmcs1,kpmcs3,0.54);
lnmcs4 = Line(kpmcs2,kpmcs4,0.54);


-- AREAS

armcs1 = HyperArea(lnmcs1,lnmcs3,lnmcs2,lnmcs4,BHiron2);


-- GRID-POINTS

Lmesh(lnmcs1,50);
Lmesh(lnmcs2,50);
Lmesh(lnmcs3,6);
Lmesh(lnmcs4,6);
