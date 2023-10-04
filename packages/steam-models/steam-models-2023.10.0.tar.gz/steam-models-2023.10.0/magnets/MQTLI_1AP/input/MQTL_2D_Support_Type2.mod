-- include-file of the support type 2 from MQTL corrector magnet/Bernhard Auchmann - 01.09.00
-- referring to: LHCMQTLB0009|2


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


-- BEAMTUNNEL

RBT = 68.5;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 7.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 3.5;		dbarbt = DBARBT*mm*shrink;

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
kpsupp_8 = [0,gcorny];
kpsupp_9 = [0,0];

kph1_1 = [xh1,yh1+rh1];
kph1_2 = [xh1,yh1-rh1];

kph2_1 = [xh2,yh2+rh2];
kph2_2 = [xh2,yh2-rh2];


-- LINES

lnsupp_1 = HyperLine(kpsupp_2,kpsupp_1,"Arc",rsupp);
lnsupp_2 = HyperLine(kpsupp_2,kpsupp_3,"Bar",hbar,0.5);
lnsupp_3 = HyperLine(kpsupp_4,kpsupp_3,"Arc",rsupp);
lnsupp_4 = Line(kpsupp_4,kpsupp_5);
lnsupp_5 = Line(kpsupp_5,kpsupp_6);
lnsupp_6 = HyperLine(kpsupp_6,kpsupp_7,"Arc",gcornr);
lnsupp_7 = Line(kpsupp_7,kpsupp_8);
lnsupp_8 = Line(kpsupp_8,kpsupp_9);
lnsupp_9 = Line(kpsupp_9,kpbt6);

lnbt1 = HyperLine(kpbt2,kpbt1,"Arc",rbt);
lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt3 = HyperLine(kpbt4,kpbt3,"Arc",rbt,0.5);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);

lnsupp_10 = Line(kpbt1,kpsupp_1);

lnh1 = HyperLine(kph1_1,kph1_2,"Circle");
lnh2 = HyperLine(kph2_1,kph2_2,"Circle");


-- AREAS

arsupp = HyperArea(lnsupp_1,lnsupp_2,lnsupp_3,lnsupp_4,lnsupp_5,lnsupp_6,lnsupp_7,lnsupp_8,lnsupp_9,lnbt5,lnbt4,lnbt3,lnbt2,lnbt1,lnsupp_10,BHiron2);

arh1 = HyperArea(lnh1,BH_air);
HyperHoleOf(arh1,arsupp);

arh2 = HyperArea(lnh2,BH_air);
HyperHoleOf(arh2,arsupp);


-- GRID-POINTS

Lmesh(lnsupp_1,20);
Lmesh(lnsupp_2,8);
Lmesh(lnsupp_3,2);
Lmesh(lnsupp_4,5);
Lmesh(lnsupp_5,4);
Lmesh(lnsupp_6,4);
Lmesh(lnsupp_7,19);
Lmesh(lnsupp_8,22);
Lmesh(lnsupp_9,6);
Lmesh(lnsupp_10,12);

Lmesh(lnh1,8);
Lmesh(lnh2,12);

Lmesh(lnbt1,9);
Lmesh(lnbt2,6);
Lmesh(lnbt3,21);
Lmesh(lnbt4,6);
Lmesh(lnbt5,9);
