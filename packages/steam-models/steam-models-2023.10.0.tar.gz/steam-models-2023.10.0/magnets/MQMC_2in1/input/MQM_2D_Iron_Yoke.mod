-- include-file of the yoke from MQM quadrupole magnet/Bernhard Auchmann
-- 03.08.00 - referring to: LHCMQM__0008|2|B


-- KEYPOINTS

kpbt1 = [beamd+rbt,0];
kpbt2 = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
kpbt3 = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
kpbt4 = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5 = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];
kpbt6 = [beamd-rbt,0];

kpyoke_1 = [ryok-hcorn1,0];
kpyoke_2 = [ryok,dcorn1];
kpyoke_3 = [ryok @ Asin(ycorn2/ryok)];
kpyoke_4 = [xcorn2,ycorn2+hcorn2];
kpyoke_5 = [xcorn2-dx,ycorn2+hcorn2+dy];
kpyoke_6 = [ryok @ Pi/2-phibar-psicorn];
kpyoke_7 = [rcorn3 @ Pi/2-phibar-psicorn];
kpyoke_8 = [rcorn3 @ Pi/2-phibar-psibar];
kpyoke_9 = [rcorn3 @ Pi/2-phibar+psibar];
kpyoke_10 = [rcorn3 @ Pi/2-phibar+psicorn];
kpyoke_11 = [ryok @ Pi/2-phibar+psicorn];
kpyoke_12 = [xar05,yar05];
kpyoke_13 = [0,ryok];
kpyoke_14 = [0,yar05];
kpyoke_15 = [0,yh1+rh1];
kpyoke_16 = [0,yh1-rh1];
kpyoke_17 = [0,0];
-- Per HAGEN
kpyoke_18 = [rh1,yh1];

kph2_1 = [xh2,yh2+rh2];
kph2_2 = [xh2,yh2-rh2];

kph3_1 = [xh3,yh3+rh3];
kph3_2 = [xh3,yh3-rh3];

kpar05h_1 = [xar05h_1,yar05h_1];
kpar05h_2 = [xar05h_3,yar05h_3];


-- LINES

lnyoke_1 = HyperLine(kpyoke_2,kpyoke_1,"CornerOut");
lnyoke_2 = HyperLine(kpyoke_3,kpyoke_2,"Arc",ryok);
lnyoke_3 = HyperLine(kpyoke_4,kpyoke_3,"CornerIn",0.6);
lnyoke_4 = Line(kpyoke_5,kpyoke_4);
lnyoke_5 = HyperLine(kpyoke_6,kpyoke_5,"Arc",ryok);
lnyoke_6 = Line(kpyoke_7,kpyoke_6);
lnyoke_7 = HyperLine(kpyoke_8,kpyoke_7,"Arc",rcorn3);
lnyoke_8 = HyperLine(kpyoke_8,kpyoke_9,"Bar",hbar,0.5);
lnyoke_9 = HyperLine(kpyoke_10,kpyoke_9,"Arc",rcorn3);
lnyoke_10 = Line(kpyoke_11,kpyoke_10);
lnyoke_11 = HyperLine(kpyoke_12,kpyoke_11,"Arc",ryok);
lnyoke_12 = Line(kpyoke_14,kpar05h_2,0.5);
lnyoke_13 = Line(kpyoke_15,kpyoke_14);
lnyoke_14 = HyperLine(kpyoke_15,kpyoke_16,"Arc",kpyoke_18);
lnyoke_15 = Line(kpyoke_16,kpyoke_17);
lnyoke_16 = Line(kpyoke_17,kpbt6);

lnar05_1 = HyperLine(kpyoke_13,kpyoke_12,"Arc",ryok,0.5);
lnar05_2 = Line(kpyoke_13,kpyoke_14);
lnar05h_1 = Line(kpyoke_12,kpar05h_1);
lnar05h_2 = Line(kpar05h_2,kpar05h_1);

lnbt1 = HyperLine(kpbt2,kpbt1,"Arc",rbt);
lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt3 = HyperLine(kpbt4,kpbt3,"Arc",rbt);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);

lnyoke_17 = Line(kpbt1,kpyoke_1);

lnh2 = HyperLine(kph2_1,kph2_2,"Circle");
lnh3 = HyperLine(kph3_1,kph3_2,"Circle");


-- AREAS

aryoke = HyperArea(lnyoke_1,lnyoke_2,lnyoke_3,lnyoke_4,lnyoke_5,lnyoke_6,lnyoke_7,lnyoke_8,lnyoke_9,lnyoke_10,lnyoke_11,lnar05h_1,lnar05h_2,lnyoke_12,lnyoke_13,lnyoke_14,lnyoke_15,lnyoke_16,lnbt5,lnbt4,lnbt3,lnbt2,lnbt1,lnyoke_17,BHiron2);

ar05 = HyperArea(lnyoke_12,lnar05h_2,lnar05h_1,lnar05_1,lnar05_2,BHiron1);

arh2 = HyperArea(lnh2,BH_air);
HyperHoleOf(arh2,aryoke);

arh3 = HyperArea(lnh3,BH_air);
HyperHoleOf(arh3,aryoke);


-- GRID-POINTS

Lmesh(lnyoke_2,7);
Lmesh(lnyoke_3,3);
Lmesh(lnyoke_8,11);
Lmesh(lnyoke_12,4);
Lmesh(lnyoke_14,7);
Lmesh(lnyoke_15,11);
Lmesh(lnyoke_16,3);
Lmesh(lnyoke_17,4);
Lmesh(lnar05_1,5);
Lmesh(lnar05_2,2);
Lmesh(lnar05h_1,1);
Lmesh(lnar05h_2,1);
Lmesh(lnh2,11);
Lmesh(lnh3,9);
Lmesh(lnbt4,4);
Lmesh(lnbt2,4);







