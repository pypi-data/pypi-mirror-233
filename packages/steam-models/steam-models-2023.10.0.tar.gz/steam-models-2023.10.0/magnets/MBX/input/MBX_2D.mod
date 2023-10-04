-- iron file for fast cycling magnet of the rhic arc dipole//PCM

-- refering to :
-- drawing 12010032


-- KEYPOINTS

-- yoke RADii
kp1 = [radin,0];
kp2 = [radout,0];
kp3 = [0,radout];
-- kp4 = [0,radin];

-- RECtangle for bus
kprec1 = [0,recdis];
kprec2 = [0,recdis+rechei];

-- HELIum passage
kpheli1 = [helix-helidi/2,heliy];
kpheli2 = [helix+helidi/2,heliy];

-- SATuration Hole
kpsath1 = [sathx-sathdi/2,sathy];
kpsath2 = [sathx+sathdi/2,sathy];

-- hole for shear PIN
kppin1 = [pinx-pindi/2,piny];
kppin2 = [pinx+pindi/2,piny];

-- APerture NOtch
kpapno1 = [0,radin+apnoh];
kpapno2 = [apnow/2,radin];

-- KEY notch
kpkey1 = [Sqrt(radout*radout-keyy*keyy),keyy];
kpkey2 = [Sqrt(radout*radout-(keyy+keyh)*(keyy+keyh)),keyy+keyh];
kpkey3 = [keyw,keyy+keyh/2];

-- HEATer notch

kpheat1 = [Sin(heatan)*(radout)+Cos(heatan)*heatw,Cos(heatan)*(radout)-Sin(heatan)*heatw];
kpheat2 = [Sin(heatan)*(radout-heath)+Cos(heatan)*heatw,Cos(heatan)*(radout-heath)-Sin(heatan)*heatw];
kpheat3 = [Sin(heatan)*(radout-heath),Cos(heatan)*(radout-heath)];
kpheat4 = [Sin(heatan)*radout,Cos(heatan)*radout];

-- SURvey notch
kpsur1 = [Sqrt(radout*radout-sury*sury),sury];
kpsur2 = [surx,Sqrt(radout*radout-surx*surx)];


-- loading FLAT
kpflat1 = [Sqrt(radout*radout-flaty*flaty),flaty];
kpflat2 = [flatx,flatny];
kpflat3 = [flatx,flatny+flath];

kpflat4 = [flatx,Sqrt(radout*radout-flatx*flatx)];




lnger1 = HyperLine(kp1,kp2,"Line");
lnger2 = HyperLine(kp3,kprec2,"Line");
lnger3 = HyperLine(kprec1,kpapno1,"Line");

lnro1 = HyperLine(kpkey1,kp2,"Arc",radout);
lnro2 = HyperLine(kpflat1,kpkey2,"Arc",radout);
lnro3 = HyperLine(kpsur1,kpflat4,"Arc",radout);
lnro4 = HyperLine(kpheat1,kpsur2,"Arc",radout);
lnro5 = HyperLine(kp3,kpheat4,"Arc",radout);

lnbar1 = HyperLine(kprec2,kprec1,"Bar",recwid/2);

lnri1 = HyperLine(kpapno2,kp1,"Arc",radin);

lnapno1 = HyperLine(kpapno2,kpapno1,"CornerOut");

lnkey1 = HyperLine(kpkey1,kpkey3,"CornerIn");
lnkey2 = HyperLine(kpkey3,kpkey2,"CornerOut");

lnheat1 = HyperLine(kpheat1,kpheat2,"Line");
lnheat2 = HyperLine(kpheat2,kpheat3,"Arc",heatw/2);
lnheat3 = HyperLine(kpheat3,kpheat4,"Line");

lnheli1 = HyperLine(kpheli1,kpheli2,"Circle");

lnsath1 = HyperLine(kpsath1,kpsath2,"Circle");

lnpin1 = HyperLine(kppin1,kppin2,"Circle");

lnsur1 = HyperLine(kpsur1,kpsur2,"CornerIn");

lnflat1 = HyperLine(kpflat1,kpflat2,"CornerIn");
lnflat2 = HyperLine(kpflat2,kpflat3,"Bar",flatw);
lnflat3 = HyperLine(kpflat3,kpflat4,"Line");

ar1 = HyperArea(lnger1,lnro1,lnkey1,lnkey2,lnro2,lnflat1,lnflat2,lnflat3,lnro3,lnsur1,lnro4,lnheat1,lnheat2,lnheat3,lnro5,lnger2,lnbar1,lnger3,lnapno1,lnri1,BHiron2);
ar2 = HyperArea(lnheli1,BH_air);
ar3 = HyperArea(lnsath1,BH_air);
ar4 = HyperArea(lnpin1,BH_air);

HyperHoleOf(ar2,ar1);
HyperHoleOf(ar3,ar1);
HyperHoleOf(ar4,ar1);

Lmesh(lnri1,25);
-- Lmesh(lnger3,3);
-- Lmesh(lnro2,3);
-- Lmesh(ln1,10);
-- Lmesh(ln3,15);
-- Lmesh(lnsl1,20);

