-- include-file of the modified insert for modified MB dipole/Christine Voellinger,Martin Aleksa - 31.08.2000
-- referring to: LHCMB__A0148|1|E and insert modification sheet
-- Checked by Bernhard Auchmann and Per Hagen 31.03.2011

-- KEYPOINTS

kpins_1 = [0,blel1+houdh+(beamd-houdw)*Tan(linsphi)];
kpins_2 = [0,linsh];
kpins_3 = [linsw,linsh];
kpins_4 = [linsw,linsh + linsnh];
kpins_4a = [lh5x-dxvar,lh5y-dyvar];
kpins_4b = [lh5x+dxvar,lh5y+dyvar];
kpins_5 = [beamd-d2-Sqrt((1-(cush1*cush1)/(blel1*blel1)))*(alel2),cush1];
kpins_6 = [linscut,yinscut1];
kpins_7 = [linscut,yinscut2];

kph1_1 = [lh1x,lh1y+lh1r];
kph1_2 = [lh1x,lh1y-lh1r];


-- LINES

lnins_1 = Line(kpins_1,kpins_2,0.65);
lnins_2 = Line(kpins_2,kpins_3,0.5);
lnins_3 = Line(kpins_3,kpins_4,0.5);
-- lnins_4 = HyperLine(kpins_4,kpins_5,"EllipticArc",alel2,blel1,0.5);
lnins_4 = HyperLine(kpins_4,kpins_4a,"EllipticArc",alel2,blel1,0.5);
lnins_4a = HyperLine(kpins_4b,kpins_4a,"Arc",-lh5r,0.5);
lnins_4b = HyperLine(kpins_4b,kpins_5,"EllipticArc",alel2,blel1,0.5);
lnins_5 = HyperLine(kpins_5,kpins_6,"EllipticArc",alel2,blel1,0.5);
lnins_6 = Line(kpins_6,kpins_7,0.5);
lnyoke_15 = Line(kpins_1,kpins_7);

lnh1 = HyperLine(kph1_1,kph1_2,"Circle",0.5);


-- AREAS

arinsert  = HyperArea(lnins_1,lnins_2,lnins_3,lnins_4,lnins_4a,lnins_4b,lnins_5,lnins_6,lnyoke_15,BHiron2);

arh1 = HyperArea(lnh1,BH_air);


-- MESH-AID

-- kprecth1_1 = [lh1x,lh1y - Sqrt(2)*3.7*lh1r];
--kprecth1_2 = [lh1x + Sqrt(2)*3.7*lh1r,lh1y];

-- lnrecth1 = HyperLine(kprecth1_1,kprecth1_2,"Rectangle");

-- arrecth1 = HyperArea(lnrecth1,BHiron2);


-- DEFINING HOLES

-- HyperHoleOf(arh1,arrecth1);
-- HyperHoleOf(arrecth1,arinsert);
HyperHoleOf(arh1,arinsert);


-- DEFINING GRID-POINTS

Lmesh(lnins_1,12);
-- Lmesh(lnins_2,4);
-- Lmesh(lnins_3,2);
-- Lmesh(lnins_4,10);
-- Lmesh(lnins_5,3);
-- Lmesh(lnins_6,3);

-- Lmesh(lnyoke_15,14);

-- Lmesh(lnrecth1,16);
Lmesh(lnh1,10);





