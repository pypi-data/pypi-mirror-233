-- include-file of the support from MO corrector magnet/Bernhard Auchmann - 01.09.00
-- referring to: LHCMO_MC0005|2|A


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


-- BEAMTUNNEL

RBT = 53.00;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 7.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 3.5;		dbarbt = DBARBT*mm*shrink;

-- OUTER FORM VARIABLES

RSUPP = 256.75;		rsupp = RSUPP*mm*shrink;

PHIBAR = 45.00;		phibar = PHIBAR*deg;

DBAR = 16.00;		dbar = DBAR*mm*shrink;
HBAR = 17.00;		hbar = HBAR*mm*shrink;

psibar = Asin(dbar/(2*rsupp));

XEDGE = 164.555;	xedge = XEDGE*mm*shrink;
yedge = Sqrt(rsupp*rsupp-xedge*xedge);

GCORNX = 145.00;	gcornx = GCORNX*mm*shrink;
GCORNY = 100.00;	gcorny = GCORNY*mm*shrink;
delt = xedge-gcornx;
GCORNR = 15.00;		gcornr = GCORNR*mm*shrink;

CORNX = 95.00;		cornx = CORNX*mm*shrink;
CORNY = 98.00;		corny = CORNY*mm*shrink;

XH1 = 177.00;		xh1 = XH1*mm*shrink;
YH1 = 135.00;		yh1 = YH1*mm*shrink;
RH1 = 6.1;		rh1 = RH1*mm*shrink;
XH2 = 219.00;		xh2 = XH2*mm*shrink;
YH2 = 70.00;		yh2 = YH2*mm*shrink;
RH2 = 10.5;		rh2 = RH2*mm*shrink;
XH3 = 177.00;		xh3 = XH3*mm*shrink;
YH3 = 92.00;		yh3 = YH3*mm*shrink;
RH3 = 22.5;		rh3 = RH3*mm*shrink;


-- * * * * * * * * * * * * * * *
-- * * * S T R U C T U R E * * *
-- * * * * * * * * * * * * * * *


-- KEYPOINTS

kpbt1 = [beamd+rbt,0];
kpbt2 = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
kpbt3 = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
kpbt4 = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5 = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];
kpbt6 = [beamd-rbt,0];

kpsupp_1 = [rsupp,0];
kpsupp_2 = [rsupp @ Pi/2-phibar-psibar];
kpsupp_3 = [rsupp @ Pi/2-phibar+psibar];
kpsupp_4 = [xedge,yedge];
kpsupp_5 = [gcornx,yedge-delt];
kpsupp_6 = [gcornx,gcorny+gcornr];
kpsupp_7 = [gcornx-gcornr,gcorny];
kpsupp_8 = [cornx,gcorny];
kpsupp_9 = [0,corny];
kpsupp_10 = [0,0];

kph1_1 = [xh1,yh1+rh1];
kph1_2 = [xh1,yh1-rh1];

kph2_1 = [xh2,yh2+rh2];
kph2_2 = [xh2,yh2-rh2];

kph3_1 = [xh3+rh3,yh3];
kph3_2 = [xh3-rh3,yh3];


-- LINES

lnsupp_1 = HyperLine(kpsupp_2,kpsupp_1,"Arc",rsupp);
lnsupp_2 = HyperLine(kpsupp_2,kpsupp_3,"Bar",hbar,0.5);
lnsupp_3 = HyperLine(kpsupp_4,kpsupp_3,"Arc",rsupp);
lnsupp_4 = Line(kpsupp_4,kpsupp_5);
lnsupp_5 = Line(kpsupp_5,kpsupp_6);
lnsupp_6 = HyperLine(kpsupp_6,kpsupp_7,"Arc",gcornr);
lnsupp_7 = Line(kpsupp_7,kpsupp_8);
lnsupp_8 = HyperLine(kpsupp_8,kpsupp_9,"CornerIn");
lnsupp_9 = Line(kpsupp_9,kpsupp_10);
lnsupp_10 = Line(kpsupp_10,kpbt6);

lnbt1 = HyperLine(kpbt2,kpbt1,"Arc",rbt);
lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt3 = HyperLine(kpbt4,kpbt3,"Arc",rbt,0.5);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);

lnsupp_11 = Line(kpbt1,kpsupp_1);

lnh1 = HyperLine(kph1_1,kph1_2,"Circle");
lnh2 = HyperLine(kph2_1,kph2_2,"Circle");
lnh3 = HyperLine(kph3_1,kph3_2,"Circle");


-- AREAS

arsupp = HyperArea(lnsupp_1,lnsupp_2,lnsupp_3,lnsupp_4,lnsupp_5,lnsupp_6,lnsupp_7,lnsupp_8,lnsupp_9,lnsupp_10,lnbt5,lnbt4,lnbt3,lnbt2,lnbt1,lnsupp_11,BHiron2);

arh1 = HyperArea(lnh1,BH_air);
HyperHoleOf(arh1,arsupp);

arh2 = HyperArea(lnh2,BH_air);
HyperHoleOf(arh2,arsupp);

arh3 = HyperArea(lnh3,BHiron5);
HyperHoleOf(arh3,arsupp);

-- GRID-POINTS

Lmesh(lnsupp_1,28);
Lmesh(lnsupp_2,9);
Lmesh(lnsupp_3,3);
Lmesh(lnsupp_4,5);
Lmesh(lnsupp_5,11);
Lmesh(lnsupp_6,5);
Lmesh(lnsupp_7,7);
Lmesh(lnsupp_8,17);
Lmesh(lnsupp_9,16);
Lmesh(lnsupp_10,8);
Lmesh(lnsupp_11,16);

Lmesh(lnh1,12);
Lmesh(lnh2,12);
Lmesh(lnh3,25);

Lmesh(lnbt1,11);
Lmesh(lnbt2,6);
Lmesh(lnbt3,17);
Lmesh(lnbt4,6);
Lmesh(lnbt5,11);
