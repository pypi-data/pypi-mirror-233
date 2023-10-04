-- include-file for the yoke of the MQ quadrupole magnet/Bernhard Auchmann - 01.08.00 
-- referring to: LHCMQ_M_0004|0|B


-- KEYPOINTS

kpbt1 = [beamd+rbt,0];
kpbt2 = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
kpbt3 = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
kpbt4 = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5 = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];
kpbt6 = [beamd-rbt,0];

kpyoke_1 = [ryok,0];
kpyoke_2 = [ryok @ Pi/2-phibar-psicorn_1];
kpyoke_3 = [rcorn @ Pi/2-phibar-psicorn_1];
kpyoke_4 = [rcorn @ Pi/2-phibar-psibar];
kpyoke_5 = [rcorn @ Pi/2-phibar+psibar];
kpyoke_6 = [rcorn @ Pi/2-phibar+psicorn_2];
kpyoke_7 = [ryok @ Pi/2-phibar+psicorn_2];
kpyoke_8 = [xar05,yar05];
kpyoke_9 = [0,ryok];
kpyoke_10 = [0,yar05];
kpyoke_11 = [0,yh1+rh1];
kpyoke_11a = [rh1,yh1];
kpyoke_12 = [0,yh1-rh1];
kpyoke_13 = [0,0];

kph2_1 = [xh2,yh2+rh2];
kph2_2 = [xh2,yh2-rh2];

kph3_1 = [xh3,yh3+rh3];
kph3_2 = [xh3,yh3-rh3];

kpar05h_1 = [xar05h_1,yar05h_1];
kpar05h_2 = [xar05h_2,yar05h_2];

kpbar_1 = [ryok @ Pi/4-psiscr];
kpbar_2 = [ryok @ Pi/4+psiscr];

-- LINES

lnyoke_1 = HyperLine(kpbar_1,kpyoke_1,"Arc",ryok);
lnyoke_2 = HyperLine(kpbar_1,kpbar_2,"Bar",hscr);
lnyoke_3 = HyperLine(kpyoke_2,kpbar_2,"Arc",ryok);
lnyoke_4 = Line(kpyoke_3,kpyoke_2);
lnyoke_5 = HyperLine(kpyoke_4,kpyoke_3,"Arc",rcorn);
lnyoke_6 = HyperLine(kpyoke_4,kpyoke_5,"Bar",hbar,0.65);
lnyoke_7 = HyperLine(kpyoke_6,kpyoke_5,"Arc",rcorn);
lnyoke_8 = Line(kpyoke_7,kpyoke_6);
lnyoke_9 = HyperLine(kpyoke_8,kpyoke_7,"Arc",ryok);
lnyoke_10 = Line(kpyoke_10,kpar05h_2,0.5);
lnyoke_11 = Line(kpyoke_11,kpyoke_10);
lnyoke_12 = HyperLine(kpyoke_11,kpyoke_12,"Arc",kpyoke_11a);
lnyoke_13 = Line(kpyoke_12,kpyoke_13,0.6);
lnyoke_14 = Line(kpyoke_13,kpbt6);

lnar05_1 = HyperLine(kpyoke_9,kpyoke_8,"Arc",ryok,0.5);
lnar05_2 = Line(kpyoke_10,kpyoke_9);
lnar05h_1 = Line(kpyoke_8,kpar05h_1);
lnar05h_2 = Line(kpar05h_2,kpar05h_1);

lnbt1 = HyperLine(kpbt2,kpbt1,"Arc",rbt);
lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt3 = HyperLine(kpbt4,kpbt3,"Arc",rbt);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);

lnyoke_15 = Line(kpbt1,kpyoke_1);

lnh2 = HyperLine(kph2_1,kph2_2,"Circle");
lnh3 = HyperLine(kph3_1,kph3_2,"Circle");


-- AREAS

aryoke = HyperArea(lnyoke_1,lnyoke_2,lnyoke_3,lnyoke_4,lnyoke_5,lnyoke_6,lnyoke_7,lnyoke_8,lnyoke_9,lnar05h_1,lnar05h_2,lnyoke_10,lnyoke_11,lnyoke_12,lnyoke_13,lnyoke_14,lnbt5,lnbt4,lnbt3,lnbt2,lnbt1,lnyoke_15,BHiron2);

ar05 = HyperArea(lnyoke_10,lnar05h_2,lnar05h_1,lnar05_1,lnar05_2,BHiron2);

arh2 = HyperArea(lnh2,BH_air);
HyperHoleOf(arh2,aryoke);

arh3 = HyperArea(lnh3,BH_air);
HyperHoleOf(arh3,aryoke);


-- GRID-POINTS

Lmesh(lnh2,8);
Lmesh(lnh3,12);

Lmesh(lnbt1,11);
Lmesh(lnbt2,6);
Lmesh(lnbt3,18);
Lmesh(lnbt4,6);
Lmesh(lnbt5,11);

Lmesh(lnar05_1,10);
Lmesh(lnar05_2,2);
Lmesh(lnar05h_1,1);
Lmesh(lnar05h_2,1);

Lmesh(lnyoke_1,22);
Lmesh(lnyoke_2,9);
Lmesh(lnyoke_3,4);
Lmesh(lnyoke_4,1);
Lmesh(lnyoke_5,3);
Lmesh(lnyoke_6,17);
Lmesh(lnyoke_7,5);
Lmesh(lnyoke_8,1);
Lmesh(lnyoke_9,5);
Lmesh(lnyoke_10,10);
Lmesh(lnyoke_11,3);
Lmesh(lnyoke_12,14);
Lmesh(lnyoke_13,24);
Lmesh(lnyoke_14,2);
Lmesh(lnyoke_15,6);
