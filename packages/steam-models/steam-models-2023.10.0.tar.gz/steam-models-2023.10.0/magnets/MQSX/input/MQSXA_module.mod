-- include-file of the module from MQSXA corrector magnet/Bernhard Auchmann
-- 30.08.00 - referring to: LHCMQSXA0001|0|A


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MQSXA_RIN  = 42.6;	mqsxa_rin  = MQSXA_RIN*mm*mshrink;
MQSXA_ROUT = 89.00;	mqsxa_rout = MQSXA_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmqsxa1 = [-mqsxa_rout,0];
kpmqsxa2 = [mqsxa_rout,0];

-- Per HAGEN
kpmqsxa12 = [0,mqsxa_rout];
kpmqsxa21 = [0,-mqsxa_rout];

kpmqsxa3 = [-mqsxa_rin,0];
kpmqsxa4 = [mqsxa_rin,0];

-- Per HAGEN
kpmqsxa34 = [0,mqsxa_rin];
kpmqsxa43 = [0,-mqsxa_rin];


-- LINES

-- Per HAGEN
-- lnmqsxa1 = HyperLine(kpmqsxa1,kpmqsxa2,"Arc",mqsxa_rout);
-- lnmqsxa2 = HyperLine(kpmqsxa3,kpmqsxa4,"Arc",mqsxa_rin);
lnmqsxa1 = HyperLine(kpmqsxa1,kpmqsxa2,"Arc",kpmqsxa12);
lnmqsxa2 = HyperLine(kpmqsxa3,kpmqsxa4,"Arc",kpmqsxa34);
lnmqsxa3 = Line(kpmqsxa1,kpmqsxa3,0.58);
lnmqsxa4 = Line(kpmqsxa2,kpmqsxa4,0.58);

-- Per HAGEN
lnmqsxa5 = HyperLine(kpmqsxa1,kpmqsxa2,"Arc",kpmqsxa21);
lnmqsxa6 = HyperLine(kpmqsxa3,kpmqsxa4,"Arc",kpmqsxa43);

-- AREAS

armqsxa1 = HyperArea(lnmqsxa1,lnmqsxa3,lnmqsxa2,lnmqsxa4,BHiron2);

-- Per HAGEN
armqsxa2 = HyperArea(lnmqsxa5,lnmqsxa4,lnmqsxa6,lnmqsxa3,BHiron2);

-- GRID-POINTS

Lmesh(lnmqsxa1,42);
Lmesh(lnmqsxa2,42);
Lmesh(lnmqsxa3,10);
Lmesh(lnmqsxa4,10);
-- Per HAGEN
Lmesh(lnmqsxa5,42);
Lmesh(lnmqsxa6,42);