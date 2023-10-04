-- include file of the coil sheet for the MB-Dipole/Bernhard Auchmann - 24.08.2000
-- referring to: LHCMB__A0021|0|B (according to instructions of Christine Voellinger)
-- Design study for use of ferro-magnetic material close to coils, not part of production
-- (comments by Bernhard Auchmann and Per Hagen 31.03.2011)


-- KEYPOINTS

kpil1r = [beamd + il1x,il1y];
kpil2r = [beamd + il2x,il2y];
kpil3r = [beamd + il3x,il3y];
kpil4r = [beamd + il4x,il4y];
kpil5r = [beamd + il5x,il5y];
kpil6r = [beamd,0] + [rcmid+ilqh+poly+ilcs @ Pi/2 - il6phi];
kpil7r = [beamd,0] + [rcmid+ilqh+poly+ilcs @ Pi/2 - il7phi];

kpol1r = [beamd + ol1x,ol1y];
kpol2r = [beamd + ol2x,ol2y];
kpol3r = [beamd + ol3x,ol3y];
kpol4r = [beamd + ol4x,ol4y];
kpol5r = [beamd,0] + [rcout+olqh+poly @ ironalpha];
kpol6r = [beamd,0] + [rcout+olqh+poly+olcsin @ ironalpha];
kpol7r = [beamd + rcout+olqh+poly,0];
kpol8r = [beamd + rcout+olqh+poly+olcsin,0];
kpol9r = [beamd + rcout+olqh+poly+olcsin+olcsout,0]; 
kpol10r = [beamd,0] + [rcout+olqh+poly+olcsin+olcsout @ ironalpha];
kpol11r = [beamd,0] + [rcout+olqh+poly+olcsin+olcsout @ Pi/2 - ol11phi];

kpil1l = [beamd - il1x,il1y];
kpil2l = [beamd - il2x,il2y];
kpil3l = [beamd - il3x,il3y];
kpil4l = [beamd - il4x,il4y];
kpil5l = [beamd - il5x,il5y];
kpil6l = [beamd,0] + [rcmid+ilqh+poly+ilcs @ Pi/2 + il6phi];
kpil7l = [beamd,0] + [rcmid+ilqh+poly+ilcs @ Pi/2 + il7phi];

kpol1l = [beamd - ol1x,ol1y];
kpol2l = [beamd - ol2x,ol2y];
kpol3l = [beamd - ol3x,ol3y];
kpol4l = [beamd - ol4x,ol4y];
kpol5l = [beamd,0] + [rcout+olqh+poly @ Pi - ironalpha];
kpol6l = [beamd,0] + [rcout+olqh+poly+olcsin @ Pi - ironalpha];
kpol7l = [beamd - (rcout+olqh+poly),0];
kpol8l = [beamd - (rcout+olqh+poly+olcsin),0];
kpol9l = [beamd - (rcout+olqh+poly+olcsin+olcsout),0]; 
kpol10l = [beamd,0] + [rcout+olqh+poly+olcsin+olcsout @ Pi - ironalpha];
kpol11l = [beamd,0] + [rcout+olqh+poly+olcsin+olcsout @ Pi/2 + ol11phi];


-- LINES

lnil1r = Line(kpil1r,kpil2r);
lnil2r = Line(kpil1r,kpil3r);
lnil3r = HyperLine(kpil3r,kpil5r,"Arc",rcmid+ilqh+poly);
lnil4r = Line(kpil5r,kpil6r);
lnil5r = HyperLine(kpil7r,kpil6r,"Arc",rcmid+ilqh+poly+ilcs);
lnil6r = HyperLine(kpil4r,kpil7r,"Arc",rcmid+ilqh+poly+ilcs);
lnil7r = Line(kpil4r,kpil2r);
lnil8r = Line(kpil3r,kpil7r);

lnol1r = Line(kpol1r,kpol2r);
lnol2r = Line(kpol1r,kpol3r);
lnol3r = HyperLine(kpol3r,kpol5r,"Arc",rcout+olqh+poly);
lnol4r = Line(kpol5r,kpol6r);
lnol5r = HyperLine(kpol6r,kpol8r,"Arc",rcout+olqh+poly+olcsin);
lnol6r = Line(kpol8r,kpol9r);
lnol7r = HyperLine(kpol10r,kpol9r,"Arc",rcout+olqh+poly+olcsin+olcsout);
lnol8r = HyperLine(kpol11r,kpol10r,"Arc",rcout+olqh+poly+olcsin+olcsout);
lnol9r = HyperLine(kpol4r,kpol11r,"Arc",rcout+olqh+poly+olcsin+olcsout);
lnol10r = Line(kpol4r,kpol2r);

lnol11r = HyperLine(kpol5r,kpol7r,"Arc",rcout+olqh+poly);
lnol12r = Line(kpol7r,kpol8r);
lnol13r = Line(kpol6r,kpol10r);
lnol14r = Line(kpol3r,kpol11r);

lnil1l = Line(kpil1l,kpil2l);
lnil2l = Line(kpil1l,kpil3l);
lnil3l = HyperLine(kpil5l,kpil3l,"Arc",rcmid+ilqh+poly);
lnil4l = Line(kpil5l,kpil6l);
lnil5l = HyperLine(kpil6l,kpil7l,"Arc",rcmid+ilqh+poly+ilcs);
lnil6l = HyperLine(kpil7l,kpil4l,"Arc",rcmid+ilqh+poly+ilcs);
lnil7l = Line(kpil4l,kpil2l);
lnil8l = Line(kpil3l,kpil7l);

lnol1l = Line(kpol1l,kpol2l);
lnol2l = Line(kpol1l,kpol3l);
lnol3l = HyperLine(kpol5l,kpol3l,"Arc",rcout+olqh+poly);
lnol4l = Line(kpol5l,kpol6l);
lnol5l = HyperLine(kpol8l,kpol6l,"Arc",rcout+olqh+poly+olcsin);
lnol6l = Line(kpol8l,kpol9l);
lnol7l = HyperLine(kpol9l,kpol10l,"Arc",rcout+olqh+poly+olcsin+olcsout);
lnol8l = HyperLine(kpol10l,kpol11l,"Arc",rcout+olqh+poly+olcsin+olcsout);
lnol9l = HyperLine(kpol11l,kpol4l,"Arc",rcout+olqh+poly+olcsin+olcsout);
lnol10l = Line(kpol4l,kpol2l);

lnol11l = HyperLine(kpol7l,kpol5l,"Arc",rcout+olqh+poly);
lnol12l = Line(kpol7l,kpol8l);
lnol13l = Line(kpol6l,kpol10l);
lnol14l = Line(kpol3l,kpol11l);


-- AREAS

aril1r = HyperArea(lnil1r,lnil2r,lnil8r,lnil6r,lnil7r,BHiron5);
aril2r = HyperArea(lnil8r,lnil3r,lnil4r,lnil5r,BHiron5);

arolout1r = HyperArea(lnol1r,lnol2r,lnol14r,lnol9r,lnol10r,BHiron5);
arolout2r = HyperArea(lnol14r,lnol3r,lnol4r,lnol13r,lnol8r,BHiron5);
arolout3r = HyperArea(lnol13r,lnol5r,lnol6r,lnol7r,BHiron5);

arolinr = HyperArea(lnol11r,lnol12r,lnol5r,lnol4r,BHiron2);

aril1 = HyperArea(lnil7l,lnil6l,lnil8l,lnil2l,lnil1l,BHiron5);
aril2 = HyperArea(lnil5l,lnil4l,lnil3l,lnil8l,BHiron5);

arolout1 = HyperArea(lnol10l,lnol9l,lnol14l,lnol2l,lnol1l,BHiron5);
arolout2 = HyperArea(lnol8l,lnol13l,lnol4l,lnol3l,lnol14l,BHiron5);
arolout3 = HyperArea(lnol7l,lnol6l,lnol5l,lnol13l,BHiron5);

arolin = HyperArea(lnol4l,lnol5l,lnol12l,lnol11l,BHiron2);

-- GRID-POINTS

-- set according to geometry
Lmesh(lnil3r ,2);		-- always same value
Lmesh(lnil5r ,2);
Lmesh(lnil3l ,2);
Lmesh(lnil5l ,2);



Lmesh(lnol5r ,15);		-- nice meshes if e.g. 1st + 2nd number = 30
Lmesh(lnol7r ,15);
Lmesh(lnol11r,15);
Lmesh(lnol5l ,15);
Lmesh(lnol7l ,15);
Lmesh(lnol11l,15);

Lmesh(lnol3r ,20);
Lmesh(lnol8r ,20);
Lmesh(lnol3l ,20);
Lmesh(lnol8l ,20);



Lmesh(lnol2r ,3);		-- first two rows one less than second two rows
Lmesh(lnol2l ,3);
Lmesh(lnol10r,4);
Lmesh(lnol10l,4);

-- pre-set
Lmesh(lnil1r,1);
Lmesh(lnil2r,8);
Lmesh(lnil4r,1);
Lmesh(lnil6r,1);
Lmesh(lnil7r,9);
Lmesh(lnil8r,1);

Lmesh(lnol1r,1);
Lmesh(lnol4r,1);
Lmesh(lnol6r,1);
Lmesh(lnol9r,1);
Lmesh(lnol12r,1);
Lmesh(lnol13r,1);
Lmesh(lnol14r,1);

Lmesh(lnil1l,1);
Lmesh(lnil2l,8);
Lmesh(lnil4l,1);
Lmesh(lnil6l,1);
Lmesh(lnil7l,9);
Lmesh(lnil8l,1);

Lmesh(lnol1l,1);
Lmesh(lnol4l,1);
Lmesh(lnol6l,1);
Lmesh(lnol9l,1);
Lmesh(lnol12l,1);
Lmesh(lnol13l,1);
Lmesh(lnol14l,1);
