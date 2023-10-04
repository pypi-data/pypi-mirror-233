-- include-file of the modules from MQTL corrector magnets/Bernhard Auchmann
-- 01.09.00 - referring to: LHCMQTLB0002|1|B


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MQTL_RIN = 37.2;	mqtl_rin = MQTL_RIN*mm*mshrink;
MQTL_ROUT = 58.7;	mqtl_rout = MQTL_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmqtl1 = [beamd-mqtl_rout,0];
kpmqtl2 = [beamd+mqtl_rout,0];
kpmqtl3 = [beamd-mqtl_rin,0];
kpmqtl4 = [beamd+mqtl_rin,0];
kpmqtl5 = [beamd,mqtl_rout];
kpmqtl6 = [beamd,mqtl_rin];


-- LINES

-- lnmqtl1 = HyperLine(kpmqtl1,kpmqtl2,"Arc",mqtl_rout);
lnmqtl1 = HyperLine(kpmqtl1,kpmqtl2,"Arc",kpmqtl5);
-- lnmqtl2 = HyperLine(kpmqtl3,kpmqtl4,"Arc",mqtl_rin);
lnmqtl2 = HyperLine(kpmqtl3,kpmqtl4,"Arc",kpmqtl6);
lnmqtl3 = Line(kpmqtl1,kpmqtl3,0.54);
lnmqtl4 = Line(kpmqtl2,kpmqtl4,0.54);


-- AREAS

armqtl1 = HyperArea(lnmqtl1,lnmqtl3,lnmqtl2,lnmqtl4,BHiron2);


-- GRID-POINTS

Lmesh(lnmqtl1,40);
Lmesh(lnmqtl2,40);
Lmesh(lnmqtl3,6);
Lmesh(lnmqtl4,6);
