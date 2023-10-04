-- include-file for the collar of the MQY quadrupole magnet/Bernhard Auchmann - 18.08.2000
-- referring to: LHCMQY__0018|2|A


-- KEYPOINTS

kpusr1 = [beamd+usr,0];
kpusr2 = [beamd+usr*Cos(usphi1-uspsi),usr*Sin(usphi1-uspsi)];
kpusr3 = [beamd+usr*Cos(usphi1+uspsi),usr*Sin(usphi1+uspsi)];
kpusr4 = [beamd+(usflaty+usflatx)*(Sqrt(2)/2),(usflaty-usflatx)*(Sqrt(2)/2)];
kpusr5 = [beamd+(usflaty+usb2d)*(Sqrt(2)/2),(usflaty-usb2d)*(Sqrt(2)/2)];
kpusr6 = [beamd+(usflaty-usb2d)*(Sqrt(2)/2),(usflaty+usb2d)*(Sqrt(2)/2)];
kpusr7 = [beamd+(usflaty-usflatx)*(Sqrt(2)/2),(usflaty+usflatx)*(Sqrt(2)/2)];
kpusr8 = [beamd+usr*Cos(usphi2-uspsi),usr*Sin(usphi2-uspsi)];
kpusr9 = [beamd+usr*Cos(usphi2+uspsi),usr*Sin(usphi2+uspsi)];

kplsr1 = [beamd+lsr1,0];
kplsr2 = [beamd+ls2x,ls2y];
kplsr3 = [beamd+ls3x,ls3y];
kplsr4 = [beamd+ls4x,ls4y];
kplsr5 = [beamd+ls5x,ls5y];
kplsr6 = [beamd+ls6x,ls6y];
kplsr7 = [beamd+ls7x,ls7y];
kplsr8 = [beamd+ls8x,ls8y];
kplsr9 = [beamd+ls9x,ls9y];

kpusmid = [beamd,usr];
kplsmid = [beamd,lsr1];

kpusl1 = [beamd-usr,0];
kpusl2 = [beamd-usr*Cos(usphi1-uspsi),usr*Sin(usphi1-uspsi)];
kpusl3 = [beamd-usr*Cos(usphi1+uspsi),usr*Sin(usphi1+uspsi)];
kpusl4 = [beamd-(usflaty+usflatx)*(Sqrt(2)/2),(usflaty-usflatx)*(Sqrt(2)/2)];
kpusl5 = [beamd-(usflaty+usb2d)*(Sqrt(2)/2),(usflaty-usb2d)*(Sqrt(2)/2)];
kpusl6 = [beamd-(usflaty-usb2d)*(Sqrt(2)/2),(usflaty+usb2d)*(Sqrt(2)/2)];
kpusl7 = [beamd-(usflaty-usflatx)*(Sqrt(2)/2),(usflaty+usflatx)*(Sqrt(2)/2)];
kpusl8 = [beamd-usr*Cos(usphi2-uspsi),usr*Sin(usphi2-uspsi)];
kpusl9 = [beamd-usr*Cos(usphi2+uspsi),usr*Sin(usphi2+uspsi)];

kplsl1 = [beamd-lsr1,0];
kplsl2 = [beamd-ls2x,ls2y];
kplsl3 = [beamd-ls3x,ls3y];
kplsl4 = [beamd-ls4x,ls4y];
kplsl5 = [beamd-ls5x,ls5y];
kplsl6 = [beamd-ls6x,ls6y];
kplsl7 = [beamd-ls7x,ls7y];
kplsl8 = [beamd-ls8x,ls8y];
kplsl9 = [beamd-ls9x,ls9y];

kpbt2 = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
kpbt3 = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
kpbt4 = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5 = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];


-- LINES

lnusr1 = Line(kplsr1,kpusr1);
lnusr2 = HyperLine(kpusr2,kpusr1,"Arc",usr);
lnusr3 = HyperLine(kpusr2,kpusr3,"Bar",usbh1);
lnusr4 = HyperLine(kpusr4,kpusr3,"Arc",usr);
lnusr5 = Line(kpusr4,kpusr5);
lnusr6 = HyperLine(kpusr5,kpusr6,"Bar",usbh2);
lnusr7 = Line(kpusr6,kpusr7);
lnusr8 = HyperLine(kpusr8,kpusr7,"Arc",usr);
lnusr9 = HyperLine(kpusr8,kpusr9,"Bar",usbh1);
lnusr10 = HyperLine(kpusmid,kpusr9,"Arc",usr);

lnlsr1 = HyperLine(kplsr2,kplsr1,"Arc",lsr1);
lnlsr2 = Line(kplsr2,kplsr3);
lnlsr3 = HyperLine(kplsr4,kplsr3,"Arc",lsr2);
lnlsr4 = Line(kplsr4,kplsr5);
lnlsr5 = HyperLine(kplsr6,kplsr5,"Arc",lsr3);
lnlsr6 = Line(kplsr6,kplsr7);
lnlsr7 = HyperLine(kplsr8,kplsr7,"Arc",lsr2);
lnlsr8 = Line(kplsr8,kplsr9);
lnlsr9 = HyperLine(kplsmid,kplsr9,"Arc",lsr1);

lnusl1 = Line(kplsl1,kpusl1);
lnusl2 = HyperLine(kpusl1,kpusl2,"Arc",usr);
lnusl3 = HyperLine(kpusl3,kpusl2,"Bar",usbh1);
lnusl4 = HyperLine(kpusl3,kpusl4,"Arc",usr);
lnusl5 = Line(kpusl4,kpusl5);
lnusl6 = HyperLine(kpusl6,kpusl5,"Bar",usbh2);
lnusl7 = Line(kpusl6,kpusl7);
lnusl8 = HyperLine(kpusl7,kpusl8,"Arc",usr);
lnusl9 = HyperLine(kpusl9,kpusl8,"Bar",usbh1);
lnusl10 = HyperLine(kpusl9,kpusmid,"Arc",usr);

lnlsl1 = HyperLine(kplsl1,kplsl2,"Arc",lsr1);
lnlsl2 = Line(kplsl2,kplsl3);
lnlsl3 = HyperLine(kplsl3,kplsl4,"Arc",lsr2);
lnlsl4 = Line(kplsl4,kplsl5);
lnlsl5 = HyperLine(kplsl6,kplsl5,"Arc",lsr3);
lnlsl6 = Line(kplsl6,kplsl7);
lnlsl7 = HyperLine(kplsl7,kplsl8,"Arc",lsr2);
lnlsl8 = Line(kplsl8,kplsl9);
lnlsl9 = HyperLine(kplsl9,kplsmid,"Arc",lsr1);

lnmid = Line(kpusmid,kplsmid);

lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);

lnclose1r = Line(kpusr2,kpusr3);
lnclose2ar = Line(kpusr5,kpbt2);
lnclose2br = Line(kpusr6,kpbt3);
lnclose3r = Line(kpusr8,kpusr9);
lnclose1l = Line(kpusl2,kpusl3);
lnclose2al = Line(kpusl5,kpbt5);
lnclose2bl = Line(kpusl6,kpbt4);
lnclose3l = Line(kpusl8,kpusl9);


-- AREAS

arclose1r = HyperArea(lnusr3,lnclose1r,BHiron5);
arclose2r = HyperArea(lnclose2ar,lnbt2,lnclose2br,lnusr6,BHiron5);
arclose3r = HyperArea(lnusr9,lnclose3r,BHiron5);
arclose1l = HyperArea(lnusl3,lnclose1l,BHiron5);
arclose2l = HyperArea(lnclose2bl,lnbt4,lnclose2al,lnusl6,BHiron5);
arclose3l = HyperArea(lnusl9,lnclose3l,BHiron5);

arcollar_r = HyperArea(lnusr1,lnusr2,lnusr3,lnusr4,lnusr5,lnusr6,lnusr7,lnusr8,lnusr9,lnusr10,lnmid,lnlsr9,lnlsr8,lnlsr7,lnlsr6,lnlsr5,lnlsr4,lnlsr3,lnlsr2,lnlsr1,BHiron5);

arcollar_l = HyperArea(lnusl10,lnusl9,lnusl8,lnusl7,lnusl6,lnusl5,lnusl4,lnusl3,lnusl2,lnusl1,lnlsl1,lnlsl2,lnlsl3,lnlsl4,lnlsl5,lnlsl6,lnlsl7,lnlsl8,lnlsl9,lnmid,BHiron6);


-- GRID-POINTS

Lmesh(lnusr1,5);
Lmesh(lnusr2,5);
Lmesh(lnusr3,6);
Lmesh(lnusr4,4);
Lmesh(lnusr5,3);
Lmesh(lnusr6,6);
Lmesh(lnusr7,4);
Lmesh(lnusr8,4);
Lmesh(lnusr9,6);
Lmesh(lnusr10,6);

Lmesh(lnusl1,5);
Lmesh(lnusl2,5);
Lmesh(lnusl3,6);
Lmesh(lnusl4,4);
Lmesh(lnusl5,3);
Lmesh(lnusl6,6);
Lmesh(lnusl7,4);
Lmesh(lnusl8,4);
Lmesh(lnusl9,6);
Lmesh(lnusl10,6);

Lmesh(lnlsl1,6);
Lmesh(lnlsl2,4);
Lmesh(lnlsl3,4);
Lmesh(lnlsl4,4);
Lmesh(lnlsl5,3);
Lmesh(lnlsl6,4);
Lmesh(lnlsl7,4);
Lmesh(lnlsl8,4);

Lmesh(lnlsr1,6);
Lmesh(lnlsr2,4);
Lmesh(lnlsr3,4);
Lmesh(lnlsr4,4);
Lmesh(lnlsr5,3);
Lmesh(lnlsr6,4);
Lmesh(lnlsr7,4);
Lmesh(lnlsr8,4);


Lmesh(lnmid,6);

Lmesh(lnbt2,6);
Lmesh(lnbt4,6);

Lmesh(lnclose1r,2);
Lmesh(lnclose2ar,1);
Lmesh(lnclose2br,1);
Lmesh(lnclose3r,2);
Lmesh(lnclose1l,2);
Lmesh(lnclose2al,1);
Lmesh(lnclose2bl,1);
Lmesh(lnclose3l,2);
