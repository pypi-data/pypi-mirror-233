-- include-file of the support type 1 from MQTL corrector magnet/Bernhard Auchmann
-- 01.09.00 - referring to: LHCMQTLB0005|2|B
-- Per HAGEN, Drawing updated to LHCMQTLB0005|2|C


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


-- BEAMTUNNEL

RBT = 68.5;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 7.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 3.5;		dbarbt = DBARBT*mm*shrink;

-- OUTER FORM VARIABLES

RSUPP = 237.75;		rsupp = RSUPP*mm*shrink;
HCORN1 = 3.00;		hcorn1 = HCORN1*mm*shrink;
DCORN1 = 20.00;		dcorn1 = DCORN1*mm*shrink;
YCORN2 = 132.925;	ycorn2 = YCORN2*mm*shrink;
XCORN2 = 167.12;	xcorn2 = XCORN2*mm*shrink;
HCORN2 = 10.005;	hcorn2 = HCORN2*mm*shrink;
PHICORN2 = 15.00;	phicorn2 = PHICORN2*deg;

k = Tan(phicorn2);
cx = xcorn2;
cy = ycorn2 + hcorn2;
a = (1+k*k);
b = (2*cy-2*k*cx);
c = (cx*cx+cy*cy-rsupp*rsupp);
p = b/a;
q = c/a;
dy = (-1)*p/2+Sqrt(p*p/4-q);
dx = k*dy;

RCORN3 = 236.75;		rcorn3 = RCORN3*mm*shrink;
DCORN3 = 10.00;		dcorn3 = DCORN3*mm*shrink;
PHIBAR = 30.00;		phibar = PHIBAR*deg;

DBAR = 52.00;		dbar = DBAR*mm*shrink;
HBAR = 27.5;		hbar = HBAR*mm*shrink;

psibar = Asin(dbar/(2*rcorn3));
psicorn = Asin((dbar/2+dcorn3)/rcorn3);

YAR05 = 231.76;		yar05 = YAR05*mm*shrink;
xar05 = Sqrt(rsupp*rsupp-yar05*yar05);

h = 0.60*mm*shrink;
d = 4.00*mm*shrink;
xar05h_1 = xar05;
yar05h_1 = yar05-h;
xar05h_2 = xar05-d;
yar05h_2 = yar05-h;
xar05h_3 = xar05-d;
yar05h_3 = yar05;

disth2 = 2.00*mm*shrink;
disth3 = 3.00*mm*shrink;

YH1 = 180.00;		yh1 = YH1*mm*shrink;
RH1 = 30.00;		rh1 = RH1*mm*shrink;
XH2 = 90.00;		xh2 = XH2*mm*shrink;
YH2 = 150.00;		yh2 = YH2*mm*shrink;
RH2 = 10.5;		rh2 = RH2*mm*shrink;
XH3 = 125.00;		xh3 = XH3*mm*shrink;
YH3 = 125.00;		yh3 = YH3*mm*shrink;
RH3 = 6.1;		rh3 = RH3*mm*shrink;


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

kpsupp_1 = [rsupp-hcorn1,0];
kpsupp_2 = [rsupp,dcorn1];
kpsupp_3 = [rsupp @ Asin(ycorn2/rsupp)];
kpsupp_4 = [xcorn2,ycorn2+hcorn2];
kpsupp_5 = [xcorn2-dx,ycorn2+hcorn2+dy];
kpsupp_6 = [rsupp @ Pi/2-phibar-psicorn];
kpsupp_7 = [rcorn3 @ Pi/2-phibar-psicorn];
kpsupp_8 = [rcorn3 @ Pi/2-phibar-psibar];
kpsupp_9 = [rcorn3 @ Pi/2-phibar+psibar];
kpsupp_10 = [rcorn3 @ Pi/2-phibar+psicorn];
kpsupp_11 = [rsupp @ Pi/2-phibar+psicorn];
kpsupp_12 = [xar05,yar05];
kpsupp_13 = [0,rsupp];
kpsupp_14 = [0,yar05];
kpsupp_15 = [0,yh1+rh1];
kpsupp_16 = [0,yh1-rh1];
kpsupp_161 = [rh1,yh1]; -- Per Hagen
kpsupp_17 = [0,0];

kph2_1 = [xh2,yh2+rh2];
kph2_2 = [xh2,yh2-rh2];

kph3_1 = [xh3,yh3+rh3];
kph3_2 = [xh3,yh3-rh3];

kpar05h_1 = [xar05h_1,yar05h_1];
kpar05h_2 = [xar05h_3,yar05h_3];


-- LINES

lnsupp_1 = HyperLine(kpsupp_2,kpsupp_1,"CornerOut");
lnsupp_2 = HyperLine(kpsupp_3,kpsupp_2,"Arc",rsupp);
lnsupp_3 = HyperLine(kpsupp_4,kpsupp_3,"CornerIn",0.6);
lnsupp_4 = Line(kpsupp_5,kpsupp_4);
lnsupp_5 = HyperLine(kpsupp_6,kpsupp_5,"Arc",rsupp);
lnsupp_6 = Line(kpsupp_7,kpsupp_6);
lnsupp_7 = HyperLine(kpsupp_8,kpsupp_7,"Arc",rcorn3);
lnsupp_8 = HyperLine(kpsupp_8,kpsupp_9,"Bar",hbar,0.5);
lnsupp_9 = HyperLine(kpsupp_10,kpsupp_9,"Arc",rcorn3);
lnsupp_10 = Line(kpsupp_11,kpsupp_10);
lnsupp_11 = HyperLine(kpsupp_12,kpsupp_11,"Arc",rsupp);
lnsupp_12 = Line(kpsupp_14,kpar05h_2,0.5);
lnsupp_13 = Line(kpsupp_15,kpsupp_14);
--lnsupp_14 = HyperLine(kpsupp_15,kpsupp_16,"Arc",rh1);
lnsupp_14 = HyperLine(kpsupp_15,kpsupp_16,"Arc",kpsupp_161);
lnsupp_15 = Line(kpsupp_16,kpsupp_17);
lnsupp_16 = Line(kpsupp_17,kpbt6);

lnar05_1 = HyperLine(kpsupp_13,kpsupp_12,"Arc",rsupp,0.5);
lnar05_2 = Line(kpsupp_13,kpsupp_14);
lnar05h_1 = Line(kpsupp_12,kpar05h_1);
lnar05h_2 = Line(kpar05h_2,kpar05h_1);

lnbt1 = HyperLine(kpbt2,kpbt1,"Arc",rbt);
lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt3 = HyperLine(kpbt4,kpbt3,"Arc",rbt);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);

lnsupp_17 = Line(kpbt1,kpsupp_1);

lnh2 = HyperLine(kph2_1,kph2_2,"Circle");
lnh3 = HyperLine(kph3_1,kph3_2,"Circle");


-- AREAS

arsupp = HyperArea(lnsupp_1,lnsupp_2,lnsupp_3,lnsupp_4,lnsupp_5,lnsupp_6,lnsupp_7,lnsupp_8,lnsupp_9,lnsupp_10,lnsupp_11,lnar05h_1,lnar05h_2,lnsupp_12,lnsupp_13,lnsupp_14,lnsupp_15,lnsupp_16,lnbt5,lnbt4,lnbt3,lnbt2,lnbt1,lnsupp_17,BHiron2);

ar05 = HyperArea(lnsupp_12,lnar05h_2,lnar05h_1,lnar05_1,lnar05_2,BHiron1);

arh2 = HyperArea(lnh2,BH_air);
HyperHoleOf(arh2,arsupp);

arh3 = HyperArea(lnh3,BH_air);
HyperHoleOf(arh3,arsupp);


-- GRID-POINTS

Lmesh(lnsupp_1,4);
Lmesh(lnsupp_2,13);
Lmesh(lnsupp_3,5);
Lmesh(lnsupp_4,5);
Lmesh(lnsupp_5,4);
Lmesh(lnsupp_6,1);
Lmesh(lnsupp_7,2);
Lmesh(lnsupp_8,16);
Lmesh(lnsupp_9,2);
Lmesh(lnsupp_10,1);
Lmesh(lnsupp_11,8);
Lmesh(lnsupp_12,8);
Lmesh(lnsupp_13,4);
Lmesh(lnsupp_14,14);
Lmesh(lnsupp_15,24);
Lmesh(lnsupp_16,6);
Lmesh(lnsupp_17,13);

Lmesh(lnar05_1,10);
Lmesh(lnar05_2,2);
Lmesh(lnar05h_1,1);
Lmesh(lnar05h_2,1);

Lmesh(lnh2,12);
Lmesh(lnh3,12);

Lmesh(lnbt1,9);
Lmesh(lnbt2,6);
Lmesh(lnbt3,21);
Lmesh(lnbt4,6);
Lmesh(lnbt5,9);



