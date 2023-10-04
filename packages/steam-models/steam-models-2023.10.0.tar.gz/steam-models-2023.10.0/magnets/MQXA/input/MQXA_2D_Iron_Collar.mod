-- include file of the collar for MQX quadrupole magnet/Bernhard Auchmann, 25.08.2000
-- referring to: 


-- KEYPOINTS

kpls1 = [lsr1,0];
kpls2 = [ls2x,ls2y];
kpls3 = [ls3x,ls3y];
kpls4 = [ls4x,ls4y];
kpls5 = [ls5x,ls5y];
kpls6 = [ls6x,ls6y];
kpls7 = [ls7x,ls7y];
kpls8 = [ls8x,ls8y];
kpls9 = [ls9x,ls9y];
kpls10 = [0,lsr1];

kpus1 = [usarc-usarcr,0];
kpus1a = [usarc,usarcr];
kpus2 = [usarc+usarcr,0];
kpus3 = [usout,0];
kpus4 = [usout,usd1];
kpus5 = [usout-usd3,usd2];
kpus6 = [usout-usd4,usd2];

kpbt2 = [rbt @ psihatbt]; 
kpbt3 = [rbt @ phibt-psihatbt]; 
kpbt4 = [rhatbt @ phibt]; 
kpbt5 = [rbt @ phibt+psihatbt]; 
kpbt6 = [rbt @ Pi/2-psihatbt]; 

kpus7 = [usd2,usout-usd4];
kpus8 = [usd2,usout-usd3];
kpus9 = [usd1,usout];
kpus10 = [0,usout];
kpus11 = [0,usarc+usarcr];
kpus11a = [usarcr,usarc];
kpus12 = [0,usarc-usarcr];

kphc1_1 = [lsharc-lshr @ Pi/4 - lshphi];
kphc1_2 = [lsharc+lshr @ Pi/4-lshphi];

kphc2_1 = [lsharc-lshr @ Pi/4+lshphi];
kphc2_2 = [lsharc+lshr @ Pi/4+lshphi];

kparc1 = [(yarc+lsr4)*Sqrt(2)/2,(yarc-lsr4)*Sqrt(2)/2];
kparc2 = [(yarc-lsr4)*Sqrt(2)/2,(yarc+lsr4)*Sqrt(2)/2];
kparcmid = [(yarc+lsr4)*Sqrt(2)/2,(yarc+lsr4)*Sqrt(2)/2];


-- LINES

lnus1 = Line(kpls1,kpus1);
lnus2 = HyperLine(kpus1,kpus2,"Arc",kpus1a);
lnus3 = Line(kpus2,kpus3);
lnus4 = Line(kpus3,kpus4);
lnus5 = Line(kpus4,kpus5);
lnus6 = Line(kpus5,kpus6);
lnus7 = HyperLine(kpbt2,kpus6,"Arc",usr);

lnbt2 = HyperLine(kpbt3,kpbt2,"Arc",rbt);
lnbt3 = Line(kpbt3,kpbt4);
lnbt4 = Line(kpbt4,kpbt5);
lnbt5 = HyperLine(kpbt6,kpbt5,"Arc",rbt);

lnus8 = HyperLine(kpus7,kpbt6,"Arc",usr);
lnus9 = Line(kpus7,kpus8);
lnus10 = Line(kpus8,kpus9);
lnus11 = Line(kpus9,kpus10);
lnus12 = Line(kpus10,kpus11);
lnus13 = HyperLine(kpus11,kpus12,"Arc",kpus11a);
lnus14 = Line(kpus12,kpls10);

lnls1 = HyperLine(kpls2,kpls1,"Arc",lsr1);
lnls2 = Line(kpls2,kpls3);
lnls3 = HyperLine(kpls4,kpls3,"Arc",lsr2);
lnls4 = Line(kpls4,kpls5);
lnls5 = HyperLine(kparc1,kpls5,"Arc",lsr3);
lnls6 = HyperLine(kparcmid,kparc1,"Arc",lsr4);
lnls7 = HyperLine(kparc2,kparcmid,"Arc",lsr4);
lnls8 = HyperLine(kpls6,kparc2,"Arc",lsr3);
lnls9 = Line(kpls6,kpls7);
lnls10 = HyperLine(kpls8,kpls7,"Arc",lsr2);
lnls11 = Line(kpls8,kpls9);
lnls12 = HyperLine(kpls10,kpls9,"Arc",lsr1);

lnhc1 = HyperLine(kphc1_1,kphc1_2,"Circle");
lnhc2 = HyperLine(kphc2_1,kphc2_2,"Circle");

lndiv = Line(kpbt4,kparcmid);


-- AREAS

arcollar_r = HyperArea(lnus1,lnus2,lnus3,lnus4,lnus5,lnus6,lnus7,lnbt2,lnbt3,lndiv,lnls6,lnls5,lnls4,lnls3,lnls2,lnls1,BHiron5);

arcollar_l = HyperArea(lnbt4,lnbt5,lnus8,lnus9,lnus10,lnus11,lnus12,lnus13,lnus14,lnls12,lnls11,lnls10,lnls9,lnls8,lnls7,lndiv,BHiron5);

arhc1 = HyperArea(lnhc1,BH_air);
arhc2 = HyperArea(lnhc2,BH_air);

HyperHoleOf(arhc1,arcollar_r);
HyperHoleOf(arhc2,arcollar_l);


-- GRID-POINTS

Lmesh(lnls1,8);
Lmesh(lnls2,6);
Lmesh(lnls3,4);
Lmesh(lnls4,6);
Lmesh(lnls5,2);
Lmesh(lnls6,1);
Lmesh(lnls7,1);
Lmesh(lnls8,2);
Lmesh(lnls9,6);
Lmesh(lnls10,4);
Lmesh(lnls11,6);
Lmesh(lnls12,8);

Lmesh(lnus1,1);
Lmesh(lnus2,3);
Lmesh(lnus3,1);
Lmesh(lnus4,1);
Lmesh(lnus5,1);
Lmesh(lnus6,1);
Lmesh(lnus7,2);
Lmesh(lnus8,2);
Lmesh(lnus9,1);
Lmesh(lnus10,1);
Lmesh(lnus11,1);
Lmesh(lnus12,1);
Lmesh(lnus13,3);
Lmesh(lnus14,1);

Lmesh(lnbt2,9);
Lmesh(lnbt3,5);
Lmesh(lnbt4,5);
Lmesh(lnbt5,9);

Lmesh(lnhc1,8);
Lmesh(lnhc2,8);

Lmesh(lndiv,16);
