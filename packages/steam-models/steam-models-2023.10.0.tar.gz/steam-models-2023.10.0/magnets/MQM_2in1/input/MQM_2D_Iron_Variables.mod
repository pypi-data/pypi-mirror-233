-- include-file of the variables from MQM quadrupole magnet/Bernhard Auchmann - 03.08.00

-- referring to: 
-- yoke		LHCMQM__0008|2|B
-- collar	LHCMQM__0015|2|B 

-- GENERAL VARIABLES

mm=0.001;
Pi=3.14159265;
deg=Pi/180;
-- Per HAGEN added design variables
dv DCONT=0.0;
shrink = 1.0*(1-DCONT);
-- 0.998
dv DCCONT=0.0;
cshrink = 1.0*(1-DCCONT);
-- 0.9973
BEAMD = 97.00;       	beamd=BEAMD*mm;

--YOKE SPECIFIC VARIABLES

-- BEAMTUNNEL

RBT = 73.4;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 9.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 3.00;		dbarbt = DBARBT*mm*shrink;

-- OUTER FORM VARIABLES

RYOK = 237.5;		ryok = RYOK*mm*shrink;
HCORN1 = 3.00;		hcorn1 = HCORN1*mm*shrink;
DCORN1 = 10.00;		dcorn1 = DCORN1*mm*shrink;
YCORN2 = 133.00;	ycorn2 = YCORN2*mm*shrink;
XCORN2 = 167.00;	xcorn2 = XCORN2*mm*shrink;
HCORN2 = 12.5;		hcorn2 = HCORN2*mm*shrink;
PHICORN2 = 10.00;	phicorn2 = PHICORN2*deg;

k = Tan(phicorn2);
cx = xcorn2;
cy = ycorn2 + hcorn2;
a = (1+k*k);
b = (2*cy-2*k*cx);
c = (cx*cx+cy*cy-ryok*ryok);
p = b/a;
q = c/a;
dy = (-1)*p/2+Sqrt(p*p/4-q);
dx = k*dy;

RCORN3 = 236.5;		rcorn3 = RCORN3*mm*shrink;
DCORN3 = 10.00;		dcorn3 = DCORN3*mm*shrink;
PHIBAR = 30.00;		phibar = PHIBAR*deg;

DBAR = 52.00;		dbar = DBAR*mm*shrink;
HBAR = 26.5;		hbar = HBAR*mm*shrink;

psibar = Asin(dbar/(2*rcorn3));
psicorn = Asin((dbar/2+dcorn3)/rcorn3);

YAR05 = 232.00;		yar05 = YAR05*mm*shrink;
xar05 = Sqrt(ryok*ryok-yar05*yar05);

h = 0.60*mm*shrink;
d = 4.00*mm*shrink;
xar05h_1 = xar05;
yar05h_1 = yar05-h;
xar05h_2 = xar05-d;
yar05h_2 = yar05-h;
xar05h_3 = xar05-d;
yar05h_3 = yar05;

disth2 = 2.00*mm*shrink;
disth3 = 3.00*mm*shrink;

YH1 = 180.00;		yh1 = YH1*mm*shrink;
RH1 = 30.00;		rh1 = RH1*mm*shrink;
XH2 = 86.5;		xh2 = XH2*mm*shrink;
YH2 = 143.00;		yh2 = YH2*mm*shrink;
RH2 = 13.00;		rh2 = RH2*mm*shrink;
XH3 = 140.00;		xh3 = XH3*mm*shrink;
YH3 = 120.00;		yh3 = YH3*mm*shrink;
RH3 = 6.1;		rh3 = RH3*mm*shrink;


-- COLLAR SPECIFIC VARIABLES


-- UPPER STRUCTURE (us)

USR = 70.40;		usr = USR*mm*cshrink;
USBH1 = 8.5;		usbh1 = USBH1*mm*cshrink;
USBH2 = 5.00;		usbh2 = USBH2*mm*cshrink;
USB1D = 4.00;		usb1d = USB1D*mm*cshrink;
USFLATY = 68.5;		usflaty = USFLATY*mm*cshrink;
USB2D = 3.00;		usb2d = USB2D*mm*cshrink;

usbs = Sqrt(usr*usr-usb1d*usb1d);
usflatx = Sqrt(usr*usr-usflaty*usflaty);


-- LOWER STRUCTURE (ls)

LSPOINT = 19.105;	lspoint = LSPOINT*mm*cshrink;
LSH = 28.00;		lsh = LSH*mm*cshrink;
LSPHI = 13.00;		lsphi = LSPHI*deg;
LSR = 47.54;		lsr = LSR*mm*cshrink;

lsrd = lsh-lspoint;

-- intersection of circle(x^2+y^2 = r^2) and line(y=kx+d)

d1 = lspoint;
k1 = 1/Tan(lsphi);
a1 = (1+k1*k1);
b1 = 2*k1*d1;
c1 = d1*d1-lsr*lsr;
lsx1 = ((-1)*b1+Sqrt(b1*b1-4*a1*c1))/(2*a1);
lsy1 = Sqrt(lsr*lsr-lsx1*lsx1); 

lsx1_45 = lsx1*(Sqrt(2)/2);
lsy1_45 = lsy1*(Sqrt(2)/2);

ls2x = lsy1_45+lsx1_45;
ls2y = lsy1_45-lsx1_45;
ls5x = lsy1_45-lsx1_45;
ls5y = lsy1_45+lsx1_45;

d2 = lspoint;
k2 = 1/Tan(lsphi);
a2 = (1+k2*k2);
b2 = 2*k2*d2;
c2 = d2*d2-lsh*lsh;
lsx2 = ((-1)*b2+Sqrt(b2*b2-4*a2*c2))/(2*a2);
lsy2 = Sqrt(lsh*lsh-lsx2*lsx2); 

lsx2_45 = lsx2*(Sqrt(2)/2);
lsy2_45 = lsy2*(Sqrt(2)/2);

ls3x = lsy2_45+lsx2_45;
ls3y = lsy2_45-lsx2_45;
ls4x = lsy2_45-lsx2_45;
ls4y = lsy2_45+lsx2_45;

