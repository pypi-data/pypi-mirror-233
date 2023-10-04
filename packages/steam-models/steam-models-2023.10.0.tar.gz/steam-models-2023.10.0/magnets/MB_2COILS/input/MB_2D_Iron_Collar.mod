-- include-file of the collar for MB dipole/Bernhard Auchmann
-- referring to: LHCMB__A0099|0|C
-- Checked 31.03.2011 by Bernhard Auchmann and Per Hagen

-- KEYPOINTS

-- COMMON KEYPOINTS WITH YOKE

kpyok_col1 = [beamd+d1+Sqrt((1-(cush1*cush1)/(blel1*blel1)))*(alel1),cush1];	-- points on ellipse 1 at: y = cush1, x = cn1x, y = cush2 
kpyok_col2 = [cn1x,Sqrt(1-((cn1x-beamd-d1)/alel1)*((cn1x-beamd-d1)/alel1))*blel1];
kpyok_col3 = [beamd+d1+Sqrt((1-(cush2*cush2)/(blel1*blel1)))*(alel1),cush2];
kpyoke_1 = [beamd+d1+alel1,0];

-- COMMON KEYPOINTS WITH INSERT

kpins_2 = [0,linsh];
kpins_3 = [linsw,linsh];
kpins_4 = [linsw,linsh + linsnh];
kpins_4a = [lh5x-dxvar,lh5y-dyvar];
kpins_4b = [lh5x+dxvar,lh5y+dyvar];
kpins_5 = [beamd-d2-Sqrt((1-(cush1*cush1)/(blel1*blel1)))*(alel2),cush1];	-- point on ellipse 2 at y = cush1 

-- US KEYPOINTS

kpusintopr = [beamd + usdin/2,ushtop];
kpusouttopr = [beamd + usdout/2,ushtop];
kpusinhinr = [beamd + (usdin/2 + (ushtop - ushin)*Tan(usphi)),ushin];
kpusouthoutr = [beamd + (usdout/2 - (ushtop - ushout)*Tan(usphi)),ushout];

kpusintopl = [beamd - usdin/2,ushtop];
kpusouttopl = [beamd - usdout/2,ushtop];
kpusinhinl = [beamd - (usdin/2 + (ushtop - ushin)*Tan(usphi)),ushin];
kpusouthoutl = [beamd - (usdout/2 - (ushtop - ushout)*Tan(usphi)),ushout];

-- LS KEYPOINTS

kplsI1 = [beamd, lshmid];

kplsI2r = [beamd + (lshmid - lshhelp2 - lsr1)*Tan(lsphi1), lshhelp2 + lsr1];
kplsI3r = [beamd + lsdI*Sin(lsphi2),lshhelp1 + lsdI*Cos(lsphi2)];

kplsI2l = [beamd - (lshmid - lshhelp2 - lsr1)*Tan(lsphi1), lshhelp2 + lsr1];
kplsI3l = [beamd - lsdI*Sin(lsphi2),lshhelp1 + lsdI*Cos(lsphi2)];

kplsII1r = [beamd + lsdIIa*Sin(lsphi2),lshhelp1 + lsdIIa*Cos(lsphi2)];
kplsII2r = [beamd + lsdIIb*Sin(lsphi3),lshhelp3 + lsdIIb*Cos(lsphi3)];
kplsIII1r = [beamd + lsdIII*Sin(lsphi3),lshhelp3 + lsdIII*Cos(lsphi3)];
kplsIII2r = [beamd + lsr3,0];

kplsII1l = [beamd - lsdIIa*Sin(lsphi2),lshhelp1 + lsdIIa*Cos(lsphi2)];
kplsII2l = [beamd - lsdIIb*Sin(lsphi3),lshhelp3 + lsdIIb*Cos(lsphi3)];
kplsIII1l = [beamd - lsdIII*Sin(lsphi3),lshhelp3 + lsdIII*Cos(lsphi3)];
kplsIII2l = [beamd - lsr3,0];

-- HOLES AND ARCS KEYPOINTS

kparc1a = [xarc1 - rarc1,0];
kparc1b = [xarc1 + rarc1,0];
kparc1c = [xarc1,rarc1];

kparc2a = [0,rarc2];
kparc2b = [rarc2,0];

kphole1a = [xhole1,yhole + rhole1];
kphole1b = [xhole1,yhole - rhole1];

kphole2a = [xhole2,yhole + rhole2];
kphole2b = [xhole2,yhole - rhole2];


-- LINES

lnyoke_21 = HyperLine(kpyok_col3,kpyoke_1,"EllipticArc",alel1,blel1,0.5);
lncorn1 = HyperLine(kpyok_col2,kpyok_col3,"CornerIn");
lnyoke_19 = HyperLine(kpyok_col1,kpyok_col2,"EllipticArc",alel1,blel1,0.5);

lnus1r = Line(kpyok_col1,kpusouthoutr);
lnus2r = Line(kpusouthoutr,kpusouttopr);
lnus3r = Line(kpusouttopr,kpusintopr);
lnus4r = Line(kpusintopr,kpusinhinr);
lnusmid = Line(kpusinhinr,kpusinhinl);
lnus4l = Line(kpusinhinl,kpusintopl);
lnus3l = Line(kpusintopl,kpusouttopl);
lnus2l = Line(kpusouttopl,kpusouthoutl);
lnus1l = Line(kpusouthoutl,kpins_5);

lnins_4 = HyperLine(kpins_4,kpins_4a,"EllipticArc",alel2,blel1,0.5);
lnins_4aa = HyperLine(kpins_4a,kpins_4b,"EllipticArc",alel2,blel1,0.5);
lnins_4b = HyperLine(kpins_4b,kpins_5,"EllipticArc",alel2,blel1,0.5);
lnins_3 = Line(kpins_3,kpins_4,0.5);
lnins_2 = Line(kpins_2,kpins_3,0.5);

lnleft1 = Line(kpins_2,kparc2a);

lnarc2 = HyperLine(kparc2a,kparc2b,"Arc",rarc2);
lnarc22 = HyperLine(kparc2a,kparc2b,"CornerIn");

lnleft2 = Line(kparc2b,kplsIII2l);

lnls1l = HyperLine(kplsIII2l,kplsIII1l,"Arc",lsr3);
lnls2l = Line(kplsIII1l,kplsII2l);
lnls3l = HyperLine(kplsII2l,kplsII1l,"Arc",lsr2);
lnls4l = Line(kplsII1l,kplsI3l);
lnls5l = HyperLine(kplsI3l,kplsI2l,"Arc",lsr1);
lnls6l = Line(kplsI2l,kplsI1);
lnls1r = HyperLine(kplsIII1r,kplsIII2r,"Arc",lsr3);
lnls2r = Line(kplsIII1r,kplsII2r);
lnls3r = HyperLine(kplsII1r,kplsII2r,"Arc",lsr2);
lnls4r = Line(kplsII1r,kplsI3r);
lnls5r = HyperLine(kplsI2r,kplsI3r,"Arc",lsr1);
lnls6r = Line(kplsI2r,kplsI1);

lnright1 = Line(kplsIII2r,kparc1a);
lnarc1 = HyperLine(kparc1a,kparc1b,"Arc",kparc1c);
lnarc11 = Line(kparc1a,kparc1b);
lnright2 = Line(kparc1b,kpyoke_1);

lnhole1 = HyperLine(kphole1a,kphole1b,"Circle");
lnhole2 = HyperLine(kphole2a,kphole2b,"Circle");


-- MESH-AID

-- lnhat = Line(kplsIII1l,kplsIII1r);


-- AREAS

-- arcollar = HyperArea(lnyoke_21,lncorn1,lnyoke_19,lnus1r,lnus2r,lnus3r,lnus4r,lnusmid,lnus4l,lnus3l,lnus2l,lnus1l,lnins_4b,lnins_4aa,lnins_4,lnins_3,lnins_2,lnleft1,lnarc2,lnleft2, lnls1l,lnhat,lnls1r,lnright1,lnarc1,lnright2,BHiron5);

arcollar = HyperArea(lnyoke_21,lncorn1,lnyoke_19,lnus1r,lnus2r,lnus3r,lnus4r,lnusmid,lnus4l,lnus3l,lnus2l,lnus1l,lnins_4b,lnins_4aa,lnins_4,lnins_3,lnins_2,lnleft1,lnarc2,lnleft2, lnls1l,lnls2l,lnls3l,lnls4l,lnls5l,lnls6l,lnls6r,lnls5r,lnls4r,lnls3r,lnls2r,lnls1r,lnright1,lnarc1,lnright2,BHiron5);

-- arhat = HyperArea(lnls2l,lnls3l,lnls4l,lnls5l,lnls6l,lnls6r,lnls5r,lnls4r,lnls3r,lnls2r,lnhat,BHiron5);

arhole1 = HyperArea(lnhole1,BHiron5);
arhole2 = HyperArea(lnhole2,BHiron5);

arpin1 = HyperArea(lnarc11,lnarc1,BHiron5); 
arpin2 = HyperArea(lnarc22,lnarc2,BHiron5); 


-- DEFINING HOLES

HyperHoleOf(arhole1,arcollar);
HyperHoleOf(arhole2,arcollar);


-- DEFINING GRID-POINTS

-- Lmesh(lnls4r,3);
-- Lmesh(lnls4l,3);
-- Lmesh(lnls2r,3);
-- Lmesh(lnls2l,3);

-- Lmesh(lnyoke_21,8);
Lmesh(lncorn1,5);
-- Lmesh(lnyoke_19,6);
Lmesh(lnus1r,5);
Lmesh(lnus2r,2);
Lmesh(lnus3r,2);
Lmesh(lnus4r,2);
Lmesh(lnusmid,5);
Lmesh(lnus4l,2);
Lmesh(lnus3l,2);
Lmesh(lnus2l,2);
Lmesh(lnus1l,5);
-- Lmesh(lnins_4,10);
-- Lmesh(lnins_3,2);
-- Lmesh(lnins_2,4);
-- Lmesh(lnleft1,10);
-- Lmesh(lnarc2,4);
-- Lmesh(lnleft2,5);
-- Lmesh(lnls1l,14);
-- Lmesh(lnhat,14);
-- Lmesh(lnls1r,12);
-- Lmesh(lnright1,3);
-- Lmesh(lnarc1,4);
-- Lmesh(lnright2,3);

Lmesh(lnhole1,8);



