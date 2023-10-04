-- include-file for the collar of the MQM quadrupole magnet/Bernhard Auchmann
-- 09.08.00 - referring to: LHCMQM__0015|2|B


-- KEYPOINTS

kplsr1 = [beamd+lsr,0];
kplsr2 = [beamd+ls2x,ls2y];
kplsr3 = [beamd+ls3x,ls3y];
kplsr4 = [beamd+ls4x,ls4y];
kplsr5 = [beamd+ls5x,ls5y];

kpusr1 = [beamd+usr-usbh1,0];
kpusr2 = [beamd+usbs,usb1d];
kpusr3 = [beamd+(usflaty+usflatx)*(Sqrt(2)/2),(usflaty-usflatx)*(Sqrt(2)/2)];
kpusr4 = [beamd+(usflaty+usb2d)*(Sqrt(2)/2),(usflaty-usb2d)*(Sqrt(2)/2)];
kpusr5 = [beamd+(usflaty-usb2d)*(Sqrt(2)/2),(usflaty+usb2d)*(Sqrt(2)/2)];
kpusr6 = [beamd+(usflaty-usflatx)*(Sqrt(2)/2),(usflaty+usflatx)*(Sqrt(2)/2)];
kpusr7 = [beamd+usb1d,usbs];

kplsl1 = [beamd-lsr,0];
kplsl2 = [beamd-ls2x,ls2y];
kplsl3 = [beamd-ls3x,ls3y];
kplsl4 = [beamd-ls4x,ls4y];
kplsl5 = [beamd-ls5x,ls5y];

kpusl1 = [beamd-usr+usbh1,0];
kpusl2 = [beamd-usbs,usb1d];
kpusl3 = [beamd-(usflaty+usflatx)*(Sqrt(2)/2),(usflaty-usflatx)*(Sqrt(2)/2)];
kpusl4 = [beamd-(usflaty+usb2d)*(Sqrt(2)/2),(usflaty-usb2d)*(Sqrt(2)/2)];
kpusl5 = [beamd-(usflaty-usb2d)*(Sqrt(2)/2),(usflaty+usb2d)*(Sqrt(2)/2)];
kpusl6 = [beamd-(usflaty-usflatx)*(Sqrt(2)/2),(usflaty+usflatx)*(Sqrt(2)/2)];
kpusl7 = [beamd-usb1d,usbs];

kpbt2 = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
kpbt3 = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
kpbt4 = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
kpbt5 = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];

-- LINES

lnusr1 = Line(kplsr1,kpusr1);
lnusr2 = HyperLine(kpusr1,kpusr2,"CornerOut");
lnusr3 = HyperLine(kpusr3,kpusr2,"Arc",usr);
lnusr4 = Line(kpusr3,kpusr4);
lnusr5 = HyperLine(kpusr4,kpusr5,"Bar",usbh2);
lnusr6 = Line(kpusr5,kpusr6);
lnusr7 = HyperLine(kpusr7,kpusr6,"Arc",usr);

lnlsr1 = HyperLine(kplsr2,kplsr1,"Arc",lsr);
lnlsr2 = Line(kplsr3,kplsr2);
lnlsr3 = HyperLine(kplsr4,kplsr3,"Arc",lsh);
lnlsr4 = Line(kplsr5,kplsr4);

lnusl1 = Line(kplsl1,kpusl1);
lnusl2 = HyperLine(kpusl1,kpusl2,"CornerOut");
lnusl3 = HyperLine(kpusl2,kpusl3,"Arc",usr);
lnusl4 = Line(kpusl3,kpusl4);
lnusl5 = HyperLine(kpusl5,kpusl4,"Bar",usbh2);
lnusl6 = Line(kpusl5,kpusl6);
lnusl7 = HyperLine(kpusl6,kpusl7,"Arc",usr);

lnlsl1 = HyperLine(kplsl1,kplsl2,"Arc",lsr);
lnlsl2 = Line(kplsl3,kplsl2);
lnlsl3 = HyperLine(kplsl3,kplsl4,"Arc",lsh);
lnlsl4 = Line(kplsl5,kplsl4);

lnusmid = HyperLine(kpusr7,kpusl7,"Bar",usbh1);
lnlsmid = HyperLine(kplsl5,kplsr5,"Arc",lsr);

lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);

lnel_y_c_r0 = HyperLine(kpusr1,kpusr2,"CornerIn");
lnel_y_c_r1a = Line(kpusr4,kpbt2);
lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
lnel_y_c_r1b = Line(kpusr5,kpbt3);
lnel_y_c_mid = Line(kpusl7,kpusr7);
lnel_y_c_l1a = Line(kpusl5,kpbt4);
lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
lnel_y_c_l1b = Line(kpusl4,kpbt5);
lnel_y_c_l0 = HyperLine(kpusl1,kpusl2,"CornerIn");

-- AREAS

ar1 = HyperArea(lnusr1,lnusr2,lnusr3,lnusr4,lnusr5,lnusr6,lnusr7,lnusmid,lnusl7,lnusl6,lnusl5,lnusl4,lnusl3,lnusl2,lnusl1,lnlsl1,lnlsl2,lnlsl3,lnlsl4,lnlsmid,lnlsr4,lnlsr3,lnlsr2,lnlsr1,BHiron5);

arel_y_c_r0 = HyperArea(lnusr2,lnel_y_c_r0,BHiron5);
arel_y_c_r1 = HyperArea(lnusr5,lnel_y_c_r1a,lnbt2,lnel_y_c_r1b,BHiron5);
arel_y_c_mid = HyperArea(lnusmid,lnel_y_c_mid,BHiron5);
arel_y_c_l1 = HyperArea(lnusl5,lnel_y_c_l1a,lnbt4,lnel_y_c_l1b,BHiron5);
arel_y_c_l0 = HyperArea(lnusl2,lnel_y_c_l0,BHiron5);


-- SET GRID-POINTS


Lmesh(lnusr2,3);
Lmesh(lnusl2,3);
Lmesh(lnusr3,8);
Lmesh(lnusl3,8);
Lmesh(lnusr5,3);
Lmesh(lnusl5,3);
Lmesh(lnusmid,6);

Lmesh(lnlsr1,8);
Lmesh(lnlsl1,8);
Lmesh(lnlsr2,5);
Lmesh(lnlsl2,5);
Lmesh(lnlsr3,3);
Lmesh(lnlsl3,3);
Lmesh(lnlsr4,5);
Lmesh(lnlsl4,5);
Lmesh(lnlsmid,16);

Lmesh(lnbt2,6);
Lmesh(lnbt4,6);