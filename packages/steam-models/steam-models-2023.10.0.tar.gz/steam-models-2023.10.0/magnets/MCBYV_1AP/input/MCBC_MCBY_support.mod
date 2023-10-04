-- include-file of the support from MCBC and MCBY corrector magnets/Bernhard Auchmann
-- 28.08.00 - referring to: LHCMCBCA0002|2|A


-- * * * * * * * * * * * * * * *
-- * * * V A R I A B L E S * * *
-- * * * * * * * * * * * * * * *


-- BEAMTUNNEL

RBT = 94.8;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 7.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 3.00;		dbarbt = DBARBT*mm*shrink;

-- OUTER FORM VARIABLES

RSUPP = 237.5;		rsupp = RSUPP*mm*shrink;
HCORN1 = 3.00;		hcorn1 = HCORN1*mm*shrink;
DCORN1 = 10.00;		dcorn1 = DCORN1*mm*shrink;
YCORN2 = 133.00;	ycorn2 = YCORN2*mm*shrink;
XCORN2 = 167.00;	xcorn2 = XCORN2*mm*shrink;
HCORN2 = 12.5;		hcorn2 = HCORN2*mm*shrink;
PHICORN2 = 10.00;	phicorn2 = PHICORN2*deg;

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

RCORN3 = 236.5;		rcorn3 = RCORN3*mm*shrink;
DCORN3 = 10.00;		dcorn3 = DCORN3*mm*shrink;
PHIBAR = 30.00;		phibar = PHIBAR*deg;

DBAR = 52.00;		dbar = DBAR*mm*shrink;
HBAR = 26.5;		hbar = HBAR*mm*shrink;

psibar = Asin(dbar/(2*rcorn3));
psicorn = Asin((dbar/2+dcorn3)/rcorn3);

YAR05 = 232.00;		yar05 = YAR05*mm*shrink;
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
XH2 = 86.5;		xh2 = XH2*mm*shrink;
YH2 = 143.00;		yh2 = YH2*mm*shrink;
RH2 = 13.00;		rh2 = RH2*mm*shrink;
XH3 = 140.00;		xh3 = XH3*mm*shrink;
YH3 = 120.00;		yh3 = YH3*mm*shrink;
RH3 = 6.1;		rh3 = RH3*mm*shrink;


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

kpsupp_1r = [rsupp-hcorn1,0];
kpsupp_2r = [rsupp,dcorn1];
kpsupp_3r = [rsupp @ Asin(ycorn2/rsupp)];
kpsupp_4r = [xcorn2,ycorn2+hcorn2];
kpsupp_5r = [xcorn2-dx,ycorn2+hcorn2+dy];
kpsupp_6r = [rsupp @ Pi/2-phibar-psicorn];
kpsupp_7r = [rcorn3 @ Pi/2-phibar-psicorn];
kpsupp_8r = [rcorn3 @ Pi/2-phibar-psibar];
kpsupp_9r = [rcorn3 @ Pi/2-phibar+psibar];
kpsupp_10r = [rcorn3 @ Pi/2-phibar+psicorn];
kpsupp_11r = [rsupp @ Pi/2-phibar+psicorn];
kpsupp_12r = [xar05,yar05];

kph2_1r = [xh2,yh2+rh2];
kph2_2r = [xh2,yh2-rh2];

kph3_1r = [xh3,yh3+rh3];
kph3_2r = [xh3,yh3-rh3];

kpar05h_1r = [xar05h_1,yar05h_1];
kpar05h_2r = [xar05h_3,yar05h_3];

-- *left*
kpbt1l = [-(beamd+rbt),0];
kpbt2l = [-(beamd+(rbt+dbarbt)*Cos(phibt)),(rbt-dbarbt)*Sin(phibt)];
kpbt3l = [-(beamd+(rbt-dbarbt)*Cos(phibt)),(rbt+dbarbt)*Sin(phibt)];
kpbt4l = [-(beamd+(rbt-dbarbt)*Cos(phibt+Pi/2)),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5l = [-(beamd+(rbt+dbarbt)*Cos(phibt+Pi/2)),(rbt-dbarbt)*Sin(phibt+Pi/2)];
kpbt6l = [-(beamd-rbt),0];

kpsupp_1l = [-(rsupp-hcorn1),0];
kpsupp_2l = [-(rsupp),dcorn1];
kpsupp_3l = [rsupp @ Pi-Asin(ycorn2/rsupp)];
kpsupp_4l = [-(xcorn2),ycorn2+hcorn2];
kpsupp_5l = [-(xcorn2-dx),ycorn2+hcorn2+dy];
kpsupp_6l = [rsupp @ Pi-(Pi/2-phibar-psicorn)];
kpsupp_7l = [rcorn3 @ Pi-(Pi/2-phibar-psicorn)];
kpsupp_8l = [rcorn3 @ Pi-(Pi/2-phibar-psibar)];
kpsupp_9l = [rcorn3 @ Pi-(Pi/2-phibar+psibar)];
kpsupp_10l = [rcorn3 @ Pi-(Pi/2-phibar+psicorn)];
kpsupp_11l = [rsupp @ Pi-(Pi/2-phibar+psicorn)];
kpsupp_12l = [-xar05,yar05];

kph2_1l = [-xh2,yh2+rh2];
kph2_2l = [-xh2,yh2-rh2];

kph3_1l = [-xh3,yh3+rh3];
kph3_2l = [-xh3,yh3-rh3];

kpar05h_1l = [-xar05h_1,yar05h_1];
kpar05h_2l = [-xar05h_3,yar05h_3];

-- *middle*
kpsupp_13 = [0,rsupp];
kpsupp_14 = [0,yar05];
kpsupp_15 = [0,yh1+rh1];
kpsupp_16 = [0,yh1-rh1];
-- Per HAGEN
kpsupp_16r = [rh1,yh1];
kpsupp_16l = [-rh1,yh1];
kpsupp_17 = [0,0];


-- LINES

-- *right*
lnsupp_1r = HyperLine(kpsupp_2r,kpsupp_1r,"CornerOut");
lnsupp_2r = HyperLine(kpsupp_3r,kpsupp_2r,"Arc",rsupp);
lnsupp_3r = HyperLine(kpsupp_4r,kpsupp_3r,"CornerIn",0.6);
lnsupp_4r = Line(kpsupp_5r,kpsupp_4r);
lnsupp_5r = HyperLine(kpsupp_6r,kpsupp_5r,"Arc",rsupp);
lnsupp_6r = Line(kpsupp_7r,kpsupp_6r);
lnsupp_7r = HyperLine(kpsupp_8r,kpsupp_7r,"Arc",rcorn3);
lnsupp_8r = HyperLine(kpsupp_8r,kpsupp_9r,"Bar",hbar,0.5);
lnsupp_9r = HyperLine(kpsupp_10r,kpsupp_9r,"Arc",rcorn3);
lnsupp_10r = Line(kpsupp_11r,kpsupp_10r);
lnsupp_11r = HyperLine(kpsupp_12r,kpsupp_11r,"Arc",rsupp);
lnsupp_12r = Line(kpsupp_14,kpar05h_2r,0.5);
-- Per HAGEN
--lnsupp_14r = HyperLine(kpsupp_15,kpsupp_16,"Arc",-rh1);
lnsupp_14r = HyperLine(kpsupp_15,kpsupp_16,"Arc",kpsupp_16r);
lnsupp_16r = Line(kpsupp_17,kpbt6r);

lnar05_1r = HyperLine(kpsupp_13,kpsupp_12r,"Arc",rsupp,0.5);
lnar05h_1r = Line(kpsupp_12r,kpar05h_1r);
lnar05h_2r = Line(kpar05h_2r,kpar05h_1r);

lnbt1r = HyperLine(kpbt2r,kpbt1r,"Arc",rbt);
lnbt2r = HyperLine(kpbt3r,kpbt2r,"Bar",hbarbt);
lnbt3r = HyperLine(kpbt4r,kpbt3r,"Arc",rbt);
lnbt4r = HyperLine(kpbt5r,kpbt4r,"Bar",hbarbt);
lnbt5r = HyperLine(kpbt6r,kpbt5r,"Arc",rbt);

lnsupp_17r = Line(kpbt1r,kpsupp_1r);

lnh2r = HyperLine(kph2_1r,kph2_2r,"Circle");
lnh3r = HyperLine(kph3_1r,kph3_2r,"Circle");

-- *left*
lnsupp_1l = HyperLine(kpsupp_2l,kpsupp_1l,"CornerOut");
lnsupp_2l = HyperLine(kpsupp_2l,kpsupp_3l,"Arc",rsupp);
lnsupp_3l = HyperLine(kpsupp_4l,kpsupp_3l,"CornerIn",0.6);
lnsupp_4l = Line(kpsupp_5l,kpsupp_4l);
lnsupp_5l = HyperLine(kpsupp_5l,kpsupp_6l,"Arc",rsupp);
lnsupp_6l = Line(kpsupp_7l,kpsupp_6l);
lnsupp_7l = HyperLine(kpsupp_7l,kpsupp_8l,"Arc",rcorn3);
lnsupp_8l = HyperLine(kpsupp_9l,kpsupp_8l,"Bar",hbar,0.5);
lnsupp_9l = HyperLine(kpsupp_9l,kpsupp_10l,"Arc",rcorn3);
lnsupp_10l = Line(kpsupp_11l,kpsupp_10l);
lnsupp_11l = HyperLine(kpsupp_11l,kpsupp_12l,"Arc",rsupp);
lnsupp_12l = Line(kpsupp_14,kpar05h_2l,0.5);
-- Per HAGEN
--lnsupp_14l = HyperLine(kpsupp_16,kpsupp_15,"Arc",-rh1);
lnsupp_14l = HyperLine(kpsupp_16,kpsupp_15,"Arc",kpsupp_16l);
lnsupp_16l = Line(kpsupp_17,kpbt6l);

lnar05_1l = HyperLine(kpsupp_12l,kpsupp_13,"Arc",rsupp,0.5);
lnar05h_1l = Line(kpsupp_12l,kpar05h_1l);
lnar05h_2l = Line(kpar05h_2l,kpar05h_1l);

lnbt1l = HyperLine(kpbt1l,kpbt2l,"Arc",rbt);
lnbt2l = HyperLine(kpbt2l,kpbt3l,"Bar",hbarbt);
lnbt3l = HyperLine(kpbt3l,kpbt4l,"Arc",rbt);
lnbt4l = HyperLine(kpbt4l,kpbt5l,"Bar",hbarbt);
lnbt5l = HyperLine(kpbt5l,kpbt6l,"Arc",rbt);

lnsupp_17l = Line(kpbt1l,kpsupp_1l);

lnh2l = HyperLine(kph2_1l,kph2_2l,"Circle");
lnh3l = HyperLine(kph3_1l,kph3_2l,"Circle");

-- *middle*
lnar05_2 = Line(kpsupp_13,kpsupp_14);
lnsupp_13 = Line(kpsupp_15,kpsupp_14);
lnsupp_15 = Line(kpsupp_16,kpsupp_17);


-- AREAS

-- *right*
arsuppr = HyperArea(lnsupp_1r,lnsupp_2r,lnsupp_3r,lnsupp_4r,lnsupp_5r,lnsupp_6r,lnsupp_7r,lnsupp_8r,lnsupp_9r,lnsupp_10r,lnsupp_11r,lnar05h_1r,lnar05h_2r,lnsupp_12r,lnsupp_13,lnsupp_14r,lnsupp_15,lnsupp_16r,lnbt5r,lnbt4r,lnbt3r,lnbt2r,lnbt1r,lnsupp_17r,BHiron2);

ar05r = HyperArea(lnsupp_12r,lnar05h_2r,lnar05h_1r,lnar05_1r,lnar05_2,BHiron1);

arh2r = HyperArea(lnh2r,BH_air);
HyperHoleOf(arh2r,arsuppr);

arh3r = HyperArea(lnh3r,BH_air);
HyperHoleOf(arh3r,arsuppr);

-- *left*
arsuppl = HyperArea(lnsupp_17l,lnbt1l,lnbt2l,lnbt3l,lnbt4l,lnbt5l,lnsupp_16l,lnsupp_15,lnsupp_14l,lnsupp_13,lnsupp_12l,lnar05h_2l,lnar05h_1l,lnsupp_11l,lnsupp_10l,lnsupp_9l,lnsupp_8l,lnsupp_7l,lnsupp_6l,lnsupp_5l,lnsupp_4l,lnsupp_3l,lnsupp_2l,lnsupp_1l,BHiron2);

ar05l = HyperArea(lnar05_2,lnar05_1l,lnar05h_1l,lnar05h_2l,lnsupp_12l,BHiron1);

arh2l = HyperArea(lnh2l,BH_air);
HyperHoleOf(arh2l,arsuppl);

arh3l = HyperArea(lnh3l,BH_air);
HyperHoleOf(arh3l,arsuppl);


-- GRID-POINTS

-- *right*
Lmesh(lnsupp_1r,3);
Lmesh(lnsupp_2r,14);
Lmesh(lnsupp_3r,5);
Lmesh(lnsupp_4r,5);
Lmesh(lnsupp_5r,4);
Lmesh(lnsupp_6r,1);
Lmesh(lnsupp_7r,2);
Lmesh(lnsupp_8r,16);
Lmesh(lnsupp_9r,2);
Lmesh(lnsupp_10r,1);
Lmesh(lnsupp_11r,8);
Lmesh(lnsupp_12r,8);
Lmesh(lnsupp_14r,14);
Lmesh(lnsupp_16r,1);
Lmesh(lnsupp_17r,8);

Lmesh(lnar05_1r,10);
Lmesh(lnar05h_1r,1);
Lmesh(lnar05h_2r,1);

Lmesh(lnh2r,12);
Lmesh(lnh3r,12);

Lmesh(lnbt1r,14);
Lmesh(lnbt2r,6);
Lmesh(lnbt3r,29);
Lmesh(lnbt4r,6);
Lmesh(lnbt5r,16);


--*left*
Lmesh(lnsupp_1l,3);
Lmesh(lnsupp_2l,14);
Lmesh(lnsupp_3l,5);
Lmesh(lnsupp_4l,5);
Lmesh(lnsupp_5l,4);
Lmesh(lnsupp_6l,1);
Lmesh(lnsupp_7l,2);
Lmesh(lnsupp_8l,16);
Lmesh(lnsupp_9l,2);
Lmesh(lnsupp_10l,1);
Lmesh(lnsupp_11l,8);
Lmesh(lnsupp_12l,8);
Lmesh(lnsupp_14l,14);
Lmesh(lnsupp_16l,1);
Lmesh(lnsupp_17l,8);

Lmesh(lnar05_1l,10);
Lmesh(lnar05h_1l,1);
Lmesh(lnar05h_2l,1);

Lmesh(lnh2l,12);
Lmesh(lnh3l,12);

Lmesh(lnbt1l,14);
Lmesh(lnbt2l,6);
Lmesh(lnbt3l,29);
Lmesh(lnbt4l,6);
Lmesh(lnbt5l,16);


-- *middle*
Lmesh(lnsupp_13,4);
Lmesh(lnsupp_15,24);
Lmesh(lnar05_2,2);



