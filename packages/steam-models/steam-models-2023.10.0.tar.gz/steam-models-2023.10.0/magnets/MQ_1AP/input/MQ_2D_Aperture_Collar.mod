-- include-file for the collar of the MQ quadrupole magnet/Bernhard Auchmann - 01.08.00
-- referring to: LHCMQ_C_0004|0|C


-- KEYPOINTS

kplsr1 = [beamd+lsr,0];
kplsr2 = [beamd+ls2x,ls2y];
kplsr3 = [beamd+ls3x,ls3y];
kplsr4 = [beamd+ls4x,ls4y];
kplsr5 = [beamd+ls5x,ls5y];

kpusr1 = [beamd+usr-usbh1,0];
kpusr2 = [beamd+usbs,usbw];
kpusr3 = [beamd+usr*Cos(usphi1-uspsi1),usr*Sin(usphi1-uspsi1)];
kpusr4 = [beamd+usr*Cos(usphi1+uspsi1),usr*Sin(usphi1+uspsi1)];
kpusr5 = [beamd+(usflaty+usflatx)*(Sqrt(2)/2),(usflaty-usflatx)*(Sqrt(2)/2)];
kpusr6 = [beamd+(usflaty+usb2d)*(Sqrt(2)/2),(usflaty-usb2d)*(Sqrt(2)/2)];
kpusr7 = [beamd+(usflaty-usb2d)*(Sqrt(2)/2),(usflaty+usb2d)*(Sqrt(2)/2)];
kpusr8 = [beamd+(usflaty-usflatx)*(Sqrt(2)/2),(usflaty+usflatx)*(Sqrt(2)/2)];
kpusr9 = [beamd+usr*Cos(usphi2-uspsi1),usr*Sin(usphi2-uspsi1)];
kpusr10 = [beamd+usr*Cos(usphi2+uspsi1),usr*Sin(usphi2+uspsi1)];
kpusr11 = [beamd+usbw,usbs];

kplsl1 = [beamd-lsr,0];
kplsl2 = [beamd-ls2x,ls2y];
kplsl3 = [beamd-ls3x,ls3y];
kplsl4 = [beamd-ls4x,ls4y];
kplsl5 = [beamd-ls5x,ls5y];

kpusl1 = [beamd-usr+usbh1,0];
kpusl2 = [beamd-usbs,usbw];
kpusl3 = [beamd-usr*Cos(usphi1-uspsi1),usr*Sin(usphi1-uspsi1)];
kpusl4 = [beamd-usr*Cos(usphi1+uspsi1),usr*Sin(usphi1+uspsi1)];
kpusl5 = [beamd-(usflaty+usflatx)*(Sqrt(2)/2),(usflaty-usflatx)*(Sqrt(2)/2)];
kpusl6 = [beamd-(usflaty+usb2d)*(Sqrt(2)/2),(usflaty-usb2d)*(Sqrt(2)/2)];
kpusl7 = [beamd-(usflaty-usb2d)*(Sqrt(2)/2),(usflaty+usb2d)*(Sqrt(2)/2)];
kpusl8 = [beamd-(usflaty-usflatx)*(Sqrt(2)/2),(usflaty+usflatx)*(Sqrt(2)/2)];
kpusl9 = [beamd-usr*Cos(usphi2-uspsi1),usr*Sin(usphi2-uspsi1)];
kpusl10 = [beamd-usr*Cos(usphi2+uspsi1),usr*Sin(usphi2+uspsi1)];
kpusl11 = [beamd-usbw,usbs];

#kpbt2 = [beamd+(rbt+dbarbt)*Cos(phibt),(rbt-dbarbt)*Sin(phibt)];
#kpbt3 = [beamd+(rbt-dbarbt)*Cos(phibt),(rbt+dbarbt)*Sin(phibt)];
#kpbt4 = [beamd+(rbt-dbarbt)*Cos(phibt+Pi/2),(rbt+dbarbt)*Sin(phibt+Pi/2)];
#kpbt5 = [beamd+(rbt+dbarbt)*Cos(phibt+Pi/2),(rbt-dbarbt)*Sin(phibt+Pi/2)];

-- LINES

lnusr1 = Line(kplsr1,kpusr1);
lnusr2 = HyperLine(kpusr1,kpusr2,"CornerOut");
lnusr3 = HyperLine(kpusr3,kpusr2,"Arc",usr);
lnusr4 = HyperLine(kpusr3,kpusr4,"Bar",usbh1);
lnusr5 = HyperLine(kpusr5,kpusr4,"Arc",usr);
lnusr6 = Line(kpusr5,kpusr6);
lnusr7 = HyperLine(kpusr6,kpusr7,"Bar",usbh2);
lnusr8 = Line(kpusr7,kpusr8);
lnusr9 = HyperLine(kpusr9,kpusr8,"Arc",usr);
lnusr10 = HyperLine(kpusr9,kpusr10,"Bar",usbh1);
lnusr11 = HyperLine(kpusr11,kpusr10,"Arc",usr);

lnlsr1 = HyperLine(kplsr2,kplsr1,"Arc",lsr);
lnlsr2 = Line(kplsr3,kplsr2);
lnlsr3 = Line(kplsr4,kplsr3);
lnlsr4 = Line(kplsr5,kplsr4);

lnusl1 = Line(kplsl1,kpusl1);
lnusl2 = HyperLine(kpusl1,kpusl2,"CornerOut");
lnusl3 = HyperLine(kpusl2,kpusl3,"Arc",usr);
lnusl4 = HyperLine(kpusl4,kpusl3,"Bar",usbh1);
lnusl5 = HyperLine(kpusl4,kpusl5,"Arc",usr);
lnusl6 = Line(kpusl5,kpusl6);
lnusl7 = HyperLine(kpusl7,kpusl6,"Bar",usbh2);
lnusl8 = Line(kpusl7,kpusl8);
lnusl9 = HyperLine(kpusl8,kpusl9,"Arc",usr);
lnusl10 = HyperLine(kpusl10,kpusl9,"Bar",usbh1);
lnusl11 = HyperLine(kpusl10,kpusl11,"Arc",usr);

lnlsl1 = HyperLine(kplsl1,kplsl2,"Arc",lsr);
lnlsl2 = Line(kplsl3,kplsl2);
lnlsl3 = Line(kplsl4,kplsl3);
lnlsl4 = Line(kplsl5,kplsl4);

lnusmid = HyperLine(kpusr11,kpusl11,"Bar",usbh1);
lnlsmid = HyperLine(kplsl5,kplsr5,"Arc",lsr);

lnardiv_r = Line(kplsr5,kpusr8);
lnardiv_l = Line(kplsl5,kpusl8);

#lnel_y_c_r0 = HyperLine(kpusr1,kpusr2,"CornerIn");
#lnel_y_c_r1 = Line(kpusr3,kpusr4);
#lnel_y_c_r2a = Line(kpusr6,kpbt2);
#lnbt2 = HyperLine(kpbt3,kpbt2,"Bar",hbarbt);
#lnel_y_c_r2b = Line(kpusr7,kpbt3);
#lnel_y_c_r3 = Line(kpusr10,kpusr9);
#lnel_y_c_mid = Line(kpusl11,kpusr11);
#lnel_y_c_l3 = Line(kpusl10,kpusl9);
#lnel_y_c_l2a = Line(kpusl7,kpbt4);
#lnbt4 = HyperLine(kpbt5,kpbt4,"Bar",hbarbt);
#lnel_y_c_l2b = Line(kpusl6,kpbt5);
#lnel_y_c_l1 = Line(kpusl3,kpusl4);
#lnel_y_c_l0 = HyperLine(kpusl1,kpusl2,"CornerIn");

-- AREAS

arcollar_r = HyperArea(lnusr1,lnusr2,lnusr3,lnusr4,lnusr5,lnusr6,lnusr7,lnusr8,lnardiv_r,lnlsr4,lnlsr3,lnlsr2,lnlsr1,BHiron5);

arcollar_mid = HyperArea(lnardiv_r,lnusr9,lnusr10,lnusr11,lnusmid,lnusl11,lnusl10,lnusl9,lnardiv_l,lnlsmid,BHiron5);

arcollar_l = HyperArea(lnardiv_l,lnusl8,lnusl7,lnusl6,lnusl5,lnusl4,lnusl3,lnusl2,lnusl1,lnlsl1,lnlsl2,lnlsl3,lnlsl4,BHiron5);

#arel_y_c_r0 = HyperArea(lnusr2,lnel_y_c_r0,BHiron5);
#arel_y_c_r1 = HyperArea(lnusr4,lnel_y_c_r1,BHiron5);
#arel_y_c_r2 = HyperArea(lnusr7,lnel_y_c_r2a,lnbt2,lnel_y_c_r2b,BHiron5);
#arel_y_c_r3 = HyperArea(lnusr10,lnel_y_c_r3,BHiron5);
#arel_y_c_mid = HyperArea(lnusmid,lnel_y_c_mid,BHiron5);
#arel_y_c_l3 = HyperArea(lnusl10,lnel_y_c_l3,BHiron5);
#arel_y_c_l2 = HyperArea(lnusl7,lnel_y_c_l2a,lnbt4,lnel_y_c_l2b,BHiron5);
#arel_y_c_l1 = HyperArea(lnusl4,lnel_y_c_l1,BHiron5);
#arel_y_c_l0 = HyperArea(lnusl2,lnel_y_c_l0,BHiron5);


-- SET GRID-POINTS

Lmesh(lnlsmid,18);
Lmesh(lnardiv_r,7);
Lmesh(lnardiv_l,7);
Lmesh(lnusmid,6);

Lmesh(lnlsr1,10);
Lmesh(lnlsr2,6);
Lmesh(lnlsr3,4);
Lmesh(lnlsr4,6);

Lmesh(lnlsl1,10);
Lmesh(lnlsl2,6);
Lmesh(lnlsl3,4);
Lmesh(lnlsl4,6);

Lmesh(lnusr1,4);
Lmesh(lnusr2,3);
Lmesh(lnusr3,6);
Lmesh(lnusr4,6);
Lmesh(lnusr5,3);
Lmesh(lnusr6,3);
Lmesh(lnusr7,6);
Lmesh(lnusr8,3);
Lmesh(lnusr9,3);
Lmesh(lnusr10,6);
Lmesh(lnusr11,7);

Lmesh(lnusl1,4);
Lmesh(lnusl2,3);
Lmesh(lnusl3,6);
Lmesh(lnusl4,6);
Lmesh(lnusl5,3);
Lmesh(lnusl6,3);
Lmesh(lnusl7,6);
Lmesh(lnusl8,3);
Lmesh(lnusl9,3);
Lmesh(lnusl10,6);
Lmesh(lnusl11,7);

#Lmesh(lnel_y_c_r1,2);
#Lmesh(lnel_y_c_l1,2);
#Lmesh(lnel_y_c_r3,2);
#Lmesh(lnel_y_c_l3,2);