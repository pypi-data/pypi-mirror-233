-- include-file of the one-piece yoke from modified MB-dipole
-- Christine Voellinger and Martin Aleksa     - 31.08.2000
-- Nose and Nick corrected by Nikolai Schwerg - 25.10.2004
-- Checked by Bernhard Auchmann and Per Hagen - 31.03.2011

-- referring to: LHCMB__A0136|0|C and LHCMB__A0133|0|C

-- KEYPOINTS

kpyoke_1 = [ beamd+d1+alel1 , 0 ];
kpyoke_2 = [ ryoke , 0 ];

kpnick_1 = [nick_x, Sqrt(ryoke*ryoke-nick_x*nick_x)];
kpnick_2 = [xnick-rnick, Sqrt(ryoke*ryoke - (xnick-rnick)*(xnick-rnick))];

kpbus_1 =  [ryoke@(phim-gammah)];
kpbus_2 =  [ryoke@(phim+gammah)];

kpnose_1 = [hx1, Sqrt(ryoke*ryoke-hx1*hx1)];
kpnose_1a = [hx2, rnose+hy];
kpnose_2 = [0,rnose];

kphhole_1 = [lhhx,lhhy+lhhr];
kphhole_2 = [lhhx+lhhr*Cos(phihco),lhhy+lhhr*Sin(phihco)];
kphhole_4 = [lhhx+lhhr*Cos(phihco),lhhy-lhhr*Sin(phihco)];
kphhole_5 = [lhhx,lhhy-lhhr];

kpins_1 = [0,blel1+houdh+(beamd-houdw)*Tan(linsphi)];
kpins_7 = [linscut,yinscut2];

kphoud_0 = [beamd-houdw,blel1+houdh];
kphoud_1 = [beamd+houdw,blel1+houdh];
kphoud_2 = [beamd+houdw+houdsh,linsh1];

kph2_1 = [lh2x,lh2y+lh2r];
kph2_2 = [lh2x,lh2y-lh2r];

kph3_1 = [lh3x,lh3y+lh3r];
kph3_2 = [lh3x,lh3y-lh3r];

kph4_1 = [lh4x,lh4y+lh4r];
kph4_2 = [lh4x,lh4y-lh4r];

kpyok_col1 = [beamd+d1+Sqrt((1-(cush1*cush1)/(blel1*blel1)))*(alel1),cush1];
kpyok_col2 = [cn1x,Sqrt(1-((cn1x-beamd-d1)/alel1)*((cn1x-beamd-d1)/alel1))*blel1];
kpyok_col3 = [beamd+d1+Sqrt((1-(cush2*cush2)/(blel1*blel1)))*(alel1),cush2];


-- LINES

lnyoke_1 = Line(kpyoke_1,kpyoke_2);
lnyoke_2 = HyperLine(kpnick_1,kpyoke_2,"Arc",ryoke,0.45);
lnyoke_3 = HyperLine(kpnick_1,kpnick_2,"Notch",Pi/2-phinick,Pi/2,0.5);
lnyoke_4 = HyperLine(kpbus_1,kpnick_2,"Arc",ryoke,0.5); 
lnyoke_5 = HyperLine(kpbus_1,kpbus_2,"Bar",bush,0.5);
lnyoke_6 = HyperLine(kpnose_1,kpbus_2,"Arc",ryoke,0.5);
lnyoke_7 = HyperLine(kpnose_1,kpnose_1a,"CornerIn",0.45);
lnyoke_8 = HyperLine(kpnose_1a,kpnose_2,"Notch",-phinos,0.,0.45);
lnyoke_9 = Line(kpnose_2,kphhole_1,0.5);
lnyoke_10= HyperLine(kphhole_1,kphhole_2,"Arc",lhhr,0.5);
lnyoke_11= HyperLine(kphhole_2,kphhole_4,"Notch",Pi/2.+phihco,Pi/2.-phihco);
lnyoke_13= HyperLine(kphhole_4,kphhole_5,"Arc",lhhr,0.5);
lnyoke_14= Line(kphhole_5,kpins_1,0.5);
lnyoke_15= Line(kpins_1,kpins_7);
lnyoke_15a = Line(kpins_7,kphoud_0);
lnyoke_16= Line(kphoud_0,kphoud_1,0.6);
lnyoke_17= Line(kphoud_1,kphoud_2,0.5);
lnyoke_18= HyperLine(kphoud_2,kpyok_col1,"EllipticArc",alel1,blel1);
lnyoke_19= HyperLine(kpyok_col1,kpyok_col2,"EllipticArc",alel1,blel1);
lnyoke_20= HyperLine(kpyok_col2,kpyok_col3,"EllipticArc",alel1,blel1);
lnyoke_21= HyperLine(kpyok_col3,kpyoke_1,"EllipticArc",alel1,blel1);

lnh2     = HyperLine(kph2_1,kph2_2,"Circle");
lnh3     = HyperLine(kph3_1,kph3_2,"Circle");
lnh4     = HyperLine(kph4_1,kph4_2,"Circle");


-- AREAS

aryoke   = HyperArea(lnyoke_1,lnyoke_2,lnyoke_3,lnyoke_4,lnyoke_5,lnyoke_6,lnyoke_7,lnyoke_8,lnyoke_9,lnyoke_10,lnyoke_11,lnyoke_13,lnyoke_14,lnyoke_15,lnyoke_15a,lnyoke_16,lnyoke_17,lnyoke_18,lnyoke_19,lnyoke_20,lnyoke_21,BHiron2);

arh2     = HyperArea(lnh2,BH_air);
arh3     = HyperArea(lnh3,BH_air);
arh4     = HyperArea(lnh4,BH_air);


-- DEFINING HOLES

HyperHoleOf(arh2,aryoke);
HyperHoleOf(arh3,aryoke);
HyperHoleOf(arh4,aryoke);


-- DEFINING GRID-POINTS

-- Lmesh(lnyoke_1,10);
Lmesh(lnyoke_2,22);
-- Lmesh(lnyoke_3,8);
-- Lmesh(lnyoke_4,5);
-- Lmesh(lnyoke_5,17);
Lmesh(lnyoke_6,14);
-- Lmesh(lnyoke_7,4);
-- Lmesh(lnyoke_9,8);
-- Lmesh(lnyoke_10,6);
-- Lmesh(lnyoke_11,6);
-- Lmesh(lnyoke_13,6);
-- Lmesh(lnyoke_14,4);
-- Lmesh(lnyoke_15,14);
-- Lmesh(lnyoke_16,8);
-- Lmesh(lnyoke_17,2);
-- Lmesh(lnyoke_18,4);
-- Lmesh(lnyoke_19,6);
-- Lmesh(lnyoke_20,3);
-- Lmesh(lnyoke_21,8);

Lmesh(lnh2,20);
-- Lmesh(lnh3,20);
-- Lmesh(lnh4,20);

