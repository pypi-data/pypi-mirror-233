-- include file of the yoke for MQX quadrupole magnet/Bernhard Auchmann, 25.08.2000
-- referring to: INSQ-M1_cross_section|A, KLHCIQ70M01-04-006


-- KEYPOINTS

kpbt1 = [rhatbt,0];
kpbt2 = [rbt @ psihatbt]; 
kpbt3 = [rbt @ phibt-psihatbt]; 
kpbt4 = [rhatbt @ phibt]; 
kpbt5 = [rbt @ phibt+psihatbt]; 
kpbt6 = [rbt @ Pi/2-psihatbt]; 
kpbt7 = [0,rhatbt];

kpyoke_1 = [xcorn1,0];
kpyoke_2 = [x2,ycorn1];
kpyoke_3 = [x3,ybar1-dbar1/2];
kpyoke_4 = [x4,ybar1+dbar1/2];
kpyoke_5 = [x5,ycorn2];
kpyoke_6 = [xcorn2,y6];
kpyoke_7 = [x7,ycorn3];
kpyoke_8 = [xcorn3,y8];
kpyoke_9 = [d1bar2/2,y9];
kpyoke_10 = [d1bar2/2,y9-h1bar2];
kpyoke_11 = [d2bar2/2,y9-h1bar2];
kpyoke_11a = [d2bar2/2+h2bar2/2,y9-h1bar2-h2bar2/2];
kpyoke_12 = [d2bar2/2,y9-h1bar2-h2bar2];
kpyoke_13 = [0,y9-h1bar2-h2bar2];

kpbarI_1 = [xcorn1+barw,0];
kpbarI_2 = [xcorn1+barw,ycorn1];

kpbarII_1 = [x4,ybar1-dbar1/2];

kpbarIII_1 = [x2,0];

kph1_1 = [dh1-rh1 @ phih1];
kph1_2 = [dh1+rh1 @ phih1];

kph2_1 = [dh2-rh2 @ phih2];
kph2_2 = [dh2+rh2 @ phih2];

kph3_1 = [dh2-rh2 @ Pi/2 - phih2];
kph3_2 = [dh2+rh2 @ Pi/2 - phih2];


-- LINES

lnbt1 = Line(kpbt1,kpbt2);
lnbt2 = HyperLine(kpbt3,kpbt2,"Arc",rbt);
lnbt3 = Line(kpbt3,kpbt4);
lnbt4 = Line(kpbt4,kpbt5);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);
lnbt6 = Line(kpbt6,kpbt7);

lnyoke_1 = Line(kpbt1,kpyoke_1,0.4);
lnyoke_2 = HyperLine(kpyoke_1,kpbarI_2,"CornerOut");
lnyoke_3 = Line(kpbarI_2,kpyoke_2);
lnyoke_4 = HyperLine(kpyoke_3,kpyoke_2,"Arc",rout);
lnyoke_5 = Line(kpyoke_3,kpbarII_1);
lnyoke_6 = HyperLine(kpbarII_1,kpyoke_4,"Bar",barw);
lnyoke_7 = HyperLine(kpyoke_5,kpyoke_4,"Arc",rout);
lnyoke_8 = HyperLine(kpyoke_6,kpyoke_5,"CornerIn");
lnyoke_9 = HyperLine(kpyoke_7,kpyoke_6,"Arc",rout);
lnyoke_10 = HyperLine(kpyoke_8,kpyoke_7,"CornerIn");
lnyoke_11 = HyperLine(kpyoke_9,kpyoke_8,"Arc",rout);
lnyoke_12 = Line(kpyoke_9,kpyoke_10);
lnyoke_13 = Line(kpyoke_10,kpyoke_11);
lnyoke_14 = HyperLine(kpyoke_12,kpyoke_11,"Arc",kpyoke_11a);
lnyoke_15 = Line(kpyoke_12,kpyoke_13);
lnyoke_16 = Line(kpyoke_13,kpbt7,0.6);

lnbarI_1 = Line(kpyoke_1,kpbarI_1);
lnbarI_2 = Line(kpbarI_1,kpbarI_2);

lnbarII_1 = Line(kpbarII_1,kpyoke_4);

lnbarIII_1 = Line(kpbarI_1,kpbarIII_1);
lnbarIII_2 = Line(kpbarIII_1,kpyoke_2);

lnh1 = HyperLine(kph1_1,kph1_2,"Circle",0.35);
lnh2 = HyperLine(kph2_1,kph2_2,"Circle");
lnh3 = HyperLine(kph3_1,kph3_2,"Circle");


-- AREA

aryoke = HyperArea(lnyoke_1,lnyoke_2,lnyoke_3,lnyoke_4,lnyoke_5,lnyoke_6,lnyoke_7,lnyoke_8,lnyoke_9,lnyoke_10,lnyoke_11,lnyoke_12,lnyoke_13,lnyoke_14,lnyoke_15,lnyoke_16,lnbt6,lnbt5,lnbt4,lnbt3,lnbt2,lnbt1,BHiron2);

arbarI = HyperArea(lnyoke_2,lnbarI_1,lnbarI_2,BHiron5);
arbarII = HyperArea(lnbarII_1,lnyoke_6,BHiron5);
arbarIII = HyperArea(lnbarI_2,lnbarIII_1,lnbarIII_2,lnyoke_3,BHiron5);


arh1 = HyperArea(lnh1,BH_air);
arh2 = HyperArea(lnh2,BH_air);
arh3 = HyperArea(lnh3,BH_air);

HyperHoleOf(arh1,aryoke);
HyperHoleOf(arh2,aryoke);
HyperHoleOf(arh3,aryoke);


-- GRID-POINTS

Lmesh(lnyoke_1,19);
Lmesh(lnyoke_2,5);
Lmesh(lnyoke_3,2);
Lmesh(lnyoke_4,3);
Lmesh(lnyoke_5,1);
Lmesh(lnyoke_6,8);
Lmesh(lnyoke_7,8);
Lmesh(lnyoke_8,7);
Lmesh(lnyoke_9,2);
Lmesh(lnyoke_10,7);
Lmesh(lnyoke_11,15);
Lmesh(lnyoke_12,2);
Lmesh(lnyoke_13,1);
Lmesh(lnyoke_14,3);
Lmesh(lnyoke_15,3);
Lmesh(lnyoke_16,19);

Lmesh(lnbarI_1,3);
Lmesh(lnbarI_2,2);
Lmesh(lnbarII_1,2);
Lmesh(lnbarIII_1,2);
Lmesh(lnbarIII_2,2);

Lmesh(lnh1,24);
Lmesh(lnh2,12);
Lmesh(lnh3,12);

Lmesh(lnbt1,5);
Lmesh(lnbt2,9);
Lmesh(lnbt3,5);
Lmesh(lnbt4,5);
Lmesh(lnbt5,9);
Lmesh(lnbt6,5);
