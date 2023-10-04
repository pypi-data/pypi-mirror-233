-- include-file of the module from MCBX corrector magnet/Bernhard Auchmann
-- 30.08.00 - referring to: LHCMCBX_0003|1


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


MCBX_RIN  = 90.00;	mcbx_rin  = MCBX_RIN*mm*mshrink;
MCBX_ROUT = 165.00;	mcbx_rout = MCBX_ROUT*mm*mshrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpmcbx1 = [-mcbx_rout,0];
kpmcbx2 = [mcbx_rout,0];
-- Per HAGEN
kpmcbx12 = [0,mcbx_rout];
kpmcbx3 = [-mcbx_rin,0];
kpmcbx4 = [mcbx_rin,0];
-- Per HAGEN
kpmcbx34 = [0,mcbx_rin];

-- Per HAGEN : Mirror x crashes so make lower part here
kpmcbx21 = [0,-mcbx_rout];
kpmcbx43 = [0,-mcbx_rin];


-- LINES

-- Per HAGEN
--lnmcbx1 = HyperLine(kpmcbx1,kpmcbx2,"Arc",mcbx_rout);
--lnmcbx2 = HyperLine(kpmcbx3,kpmcbx4,"Arc",-mcbx_rin);
lnmcbx1 = HyperLine(kpmcbx1,kpmcbx2,"Arc",kpmcbx12);
lnmcbx2 = HyperLine(kpmcbx3,kpmcbx4,"Arc",kpmcbx34);
lnmcbx3 = Line(kpmcbx1,kpmcbx3,0.58);
lnmcbx4 = Line(kpmcbx2,kpmcbx4,0.58);

-- Per HAGEN : mirrox crashes so make lower part here

lnmcbx5 = HyperLine(kpmcbx1,kpmcbx2,"Arc",kpmcbx21);
lnmcbx6 = HyperLine(kpmcbx3,kpmcbx4,"Arc",kpmcbx43);


-- AREAS

armcbx1 = HyperArea(lnmcbx1,lnmcbx3,lnmcbx2,lnmcbx4,BHiron2);

-- Per HAGEN : mirrox crashes so make lower part here
armcbx2 = HyperArea(lnmcbx3,lnmcbx5,lnmcbx4,lnmcbx6,BHiron2);

-- GRID-POINTS

Lmesh(lnmcbx1,42);
Lmesh(lnmcbx2,42);
Lmesh(lnmcbx3,8);
Lmesh(lnmcbx4,8);

-- Per HAGEN : mirrox crashes so make lower part here
Lmesh(lnmcbx5,42);
Lmesh(lnmcbx6,42);
