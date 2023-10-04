-- include-file of the support from MSCB dipole and sextupole corrector magnet/Bernhard Auchmann - 28.08.00
-- referring to: LHCMSCBA0002|2|A


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


-- BEAMTUNNEL

RBT = 94.80;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 7.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 4.00;		dbarbt = DBARBT*mm*shrink;

-- OUTER FORM VARIABLES

RSUPP = 226.00;		rsupp = RSUPP*mm*shrink;

PHIBAR = 45.00;		phibar = PHIBAR*deg;

DBAR = 16.00;		dbar = DBAR*mm*shrink;
HBAR = 17.00;		hbar = HBAR*mm*shrink;

psibar = Asin(dbar/(2*rsupp));

YEDGE = 173.00;		yedge = YEDGE*mm*shrink;
xedge = Sqrt(rsupp*rsupp-yedge*yedge);

GCORNX = 125.00;	gcornx = GCORNX*mm*shrink;
GCORNY = 125.00;	gcorny = GCORNY*mm*shrink;
delt = xedge-gcornx;
GCORNR = 10.00;		gcornr = GCORNR*mm*shrink;

XH1 = 115.00;		xh1 = XH1*mm*shrink;
YH1 = 110.00;		yh1 = YH1*mm*shrink;
RH1 = 6.1;		rh1 = RH1*mm*shrink;
XH2 = 187.00;		xh2 = XH2*mm*shrink;
YH2 = 80.00;		yh2 = YH2*mm*shrink;
RH2 = 10.5;		rh2 = RH2*mm*shrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

-- *right*
kpbt1r = [beamd+rbt,0];
kpbt2r = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
kpbt3r = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
kpbt4r = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5r = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];
kpbt6r = [beamd-rbt,0];

kpsupp_1r = [rsupp,0];
kpsupp_2r = [rsupp @ Pi/2-phibar-psibar];
kpsupp_3r = [rsupp @ Pi/2-phibar+psibar];
kpsupp_4r = [xedge,yedge];
kpsupp_5r = [gcornx,yedge-delt];
kpsupp_6r = [gcornx,gcorny+gcornr];
kpsupp_7r = [gcornx-gcornr,gcorny];

kph1_1r = [xh1,yh1+rh1];
kph1_2r = [xh1,yh1-rh1];

kph2_1r = [xh2,yh2+rh2];
kph2_2r = [xh2,yh2-rh2];

-- *left*
kpbt1l = [-(beamd+rbt),0];
kpbt2l = [-(beamd+(rbt+dbarbt)*Cos(phibt)),(rbt-dbarbt)*Sin(phibt)];
kpbt3l = [-(beamd+(rbt-dbarbt)*Cos(phibt)),(rbt+dbarbt)*Sin(phibt)];
kpbt4l = [-(beamd+(rbt-dbarbt)*Cos(phibt+Pi/2)),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5l = [-(beamd+(rbt+dbarbt)*Cos(phibt+Pi/2)),(rbt-dbarbt)*Sin(phibt+Pi/2)];
kpbt6l = [-(beamd-rbt),0];

kpsupp_1l = [-(rsupp),0];
kpsupp_2l = [rsupp @ Pi-(Pi/2-phibar-psibar)];
kpsupp_3l = [rsupp @ Pi-(Pi/2-phibar+psibar)];
kpsupp_4l = [-(xedge),yedge];
kpsupp_5l = [-(gcornx),yedge-delt];
kpsupp_6l = [-(gcornx),gcorny+gcornr];
kpsupp_7l = [-(gcornx-gcornr),gcorny];

kph1_1l = [-(xh1),yh1+rh1];
kph1_2l = [-(xh1),yh1-rh1];

kph2_1l = [-(xh2),yh2+rh2];
kph2_2l = [-(xh2),yh2-rh2];

-- *middle*
kpsupp_8 = [0,gcorny];
kpsupp_9 = [0,0];


-- LINES

-- *right*
lnsupp_1r = HyperLine(kpsupp_2r,kpsupp_1r,"Arc",rsupp);
lnsupp_2r = HyperLine(kpsupp_2r,kpsupp_3r,"Bar",hbar,0.5);
lnsupp_3r = HyperLine(kpsupp_4r,kpsupp_3r,"Arc",rsupp);
lnsupp_4r = Line(kpsupp_4r,kpsupp_5r);
lnsupp_5r = Line(kpsupp_5r,kpsupp_6r);
lnsupp_6r = HyperLine(kpsupp_6r,kpsupp_7r,"Arc",gcornr);
lnsupp_7r = Line(kpsupp_7r,kpsupp_8);
lnsupp_9r = Line(kpsupp_9,kpbt6r);

lnbt1r = HyperLine(kpbt2r,kpbt1r,"Arc",rbt);
lnbt2r = HyperLine(kpbt3r,kpbt2r,"Bar",hbarbt);
lnbt3r = HyperLine(kpbt4r,kpbt3r,"Arc",rbt,0.5);
lnbt4r = HyperLine(kpbt5r,kpbt4r,"Bar",hbarbt);
lnbt5r = HyperLine(kpbt6r,kpbt5r,"Arc",rbt);

lnsupp_10r = Line(kpbt1r,kpsupp_1r);

lnh1r = HyperLine(kph1_1r,kph1_2r,"Circle");
lnh2r = HyperLine(kph2_1r,kph2_2r,"Circle");

-- *left*
lnsupp_1l = HyperLine(kpsupp_1l,kpsupp_2l,"Arc",rsupp);
lnsupp_2l = HyperLine(kpsupp_3l,kpsupp_2l,"Bar",hbar,0.5);
lnsupp_3l = HyperLine(kpsupp_3l,kpsupp_4l,"Arc",rsupp);
lnsupp_4l = Line(kpsupp_4l,kpsupp_5l);
lnsupp_5l = Line(kpsupp_5l,kpsupp_6l);
lnsupp_6l = HyperLine(kpsupp_7l,kpsupp_6l,"Arc",gcornr);
lnsupp_7l = Line(kpsupp_7l,kpsupp_8);
lnsupp_9l = Line(kpsupp_9,kpbt6l);

lnbt1l = HyperLine(kpbt1l,kpbt2l,"Arc",rbt);
lnbt2l = HyperLine(kpbt2l,kpbt3l,"Bar",hbarbt);
lnbt3l = HyperLine(kpbt3l,kpbt4l,"Arc",rbt,0.5);
lnbt4l = HyperLine(kpbt4l,kpbt5l,"Bar",hbarbt);
lnbt5l = HyperLine(kpbt5l,kpbt6l,"Arc",rbt);

lnsupp_10l = Line(kpbt1l,kpsupp_1l);

lnh1l = HyperLine(kph1_1l,kph1_2l,"Circle");
lnh2l = HyperLine(kph2_1l,kph2_2l,"Circle");

-- *middle*
lnsupp_8 = HyperLine(kpsupp_8,kpsupp_9,"Line",0.65);


-- AREAS

-- *right*
arsuppr = HyperArea(lnsupp_1r,lnsupp_2r,lnsupp_3r,lnsupp_4r,lnsupp_5r,lnsupp_6r,lnsupp_7r,lnsupp_8,lnsupp_9r,lnbt5r,lnbt4r,lnbt3r,lnbt2r,lnbt1r,lnsupp_10r,BHiron2);

arh1r = HyperArea(lnh1r,BH_air);
HyperHoleOf(arh1r,arsuppr);

arh2r = HyperArea(lnh2r,BH_air);
HyperHoleOf(arh2r,arsuppr);

-- *left*
arsuppl = HyperArea(lnsupp_10l,lnbt1l,lnbt2l,lnbt3l,lnbt4l,lnbt5l,lnsupp_9l,lnsupp_8,lnsupp_7l,lnsupp_6l,lnsupp_5l,lnsupp_4l,lnsupp_3l,lnsupp_2l,lnsupp_1l,BHiron2);

arh1l = HyperArea(lnh1l,BH_air);
HyperHoleOf(arh1l,arsuppl);

arh2l = HyperArea(lnh2l,BH_air);
HyperHoleOf(arh2l,arsuppl);


-- GRID-POINTS

-- *right*
-- Lmesh(lnsupp_1r,20);
-- Lmesh(lnsupp_2r,8);
-- Lmesh(lnsupp_3r,2);
-- Lmesh(lnsupp_4r,5);
-- Lmesh(lnsupp_5r,4);
-- Lmesh(lnsupp_6r,4);
-- Lmesh(lnsupp_7r,19);
-- Lmesh(lnsupp_9r,2);
-- Lmesh(lnsupp_10r,6);

Lmesh(lnh1r,14);
Lmesh(lnh2r,14);

-- Lmesh(lnbt1r,14);
-- Lmesh(lnbt2r,6);
-- Lmesh(lnbt3r,23);
-- Lmesh(lnbt4r,6);
Lmesh(lnbt5r,20);

-- *left*
-- Lmesh(lnsupp_1l,20);
-- Lmesh(lnsupp_2l,8);
-- Lmesh(lnsupp_3l,2);
-- Lmesh(lnsupp_4l,5);
-- Lmesh(lnsupp_5l,4);
-- Lmesh(lnsupp_6l,4);
-- Lmesh(lnsupp_7l,19);
-- Lmesh(lnsupp_9l,2);
-- Lmesh(lnsupp_10l,6);

Lmesh(lnh1l,14);
Lmesh(lnh2l,14);

-- Lmesh(lnbt1l,14);
-- Lmesh(lnbt2l,6);
-- Lmesh(lnbt3l,23);
-- Lmesh(lnbt4l,6);
Lmesh(lnbt5l,20);

-- *middle*
Lmesh(lnsupp_8,34);
