-- include-file of the modules from MQT and MQS corrector magnets/Bernhard Auchmann
-- 01.09.00 - referring to: LHCMQT_C0002|1|B, LHCMQS_A0002|1|B


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MQTMQS_RIN = 37.2;	mqtmqs_rin = MQTMQS_RIN*mm*mshrink;
MQTMQS_ROUT = 58.7;	mqtmqs_rout = MQTMQS_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmqtmqs1 = [beamd-mqtmqs_rout,0];
kpmqtmqs2 = [beamd+mqtmqs_rout,0];
kpmqtmqs3 = [beamd-mqtmqs_rin,0];
kpmqtmqs4 = [beamd+mqtmqs_rin,0];


-- LINES

lnmqtmqs1 = HyperLine(kpmqtmqs1,kpmqtmqs2,"Arc",mqtmqs_rout);
lnmqtmqs2 = HyperLine(kpmqtmqs3,kpmqtmqs4,"Arc",mqtmqs_rin);
lnmqtmqs3 = Line(kpmqtmqs1,kpmqtmqs3,0.54);
lnmqtmqs4 = Line(kpmqtmqs2,kpmqtmqs4,0.54);


-- AREAS

armqtmqs1 = HyperArea(lnmqtmqs1,lnmqtmqs3,lnmqtmqs2,lnmqtmqs4,BHiron2);


-- GRID-POINTS

Lmesh(lnmqtmqs1,40);
Lmesh(lnmqtmqs2,40);
Lmesh(lnmqtmqs3,6);
Lmesh(lnmqtmqs4,6);
