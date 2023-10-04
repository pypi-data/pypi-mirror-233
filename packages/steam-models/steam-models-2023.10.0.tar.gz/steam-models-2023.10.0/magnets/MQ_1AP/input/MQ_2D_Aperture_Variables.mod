-- include-file for variables of MQ main quadrupole iron-files/Bernhard Auchmann - 01.08.00

-- referring to: 
-- yoke		LHCMQ_M_0004|0|B
-- collar	LHCMQ_C_0004|0|C


-- GENERAL VARIABLES

mm=0.001;
Pi=3.14159265;
deg=Pi/180;
dv DCONT = 0.0;
shrink = 1.0*(1.-DCONT);
cshrink = 1.0*(1.-DCONT);
BEAMD = 97.00;       	beamd=BEAMD*mm;


-- YOKE SPECIFIC VARIABLES


-- BEAMTUNNEL

RBT = 90.00;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 7.00;		hbarbt = HBARBT*mm*shrink;
DBARBT = 4.00;		dbarbt = DBARBT*mm*shrink;
-- Per HAGEN 13.08.2010: DBARBT changed from 3.00 to 4.00
-- pin holes 8 mm according to drawing LHCMQ_M_004|0|B


-- OUTER FORM VARIABLES

RYOK = 226.00;		ryok = RYOK*mm*shrink;

-- busbar and corners for fermeture 

RCORN = 225.00;		rcorn = RCORN*mm*shrink;
DCORN_1 = 9.5;		dcorn_1 = DCORN_1*mm*shrink;
DCORN_2 = 19.5;		dcorn_2 = DCORN_2*mm*shrink;
PHIBAR = 30.00;		phibar = PHIBAR*deg;

DBAR = 51.00;		dbar = DBAR*mm*shrink;
HBAR = 25.00;		hbar = HBAR*mm*shrink;

psibar = Asin(dbar/(2*rcorn));
psicorn_1 = Asin((dbar/2+dcorn_1)/rcorn);
psicorn_2 = Asin((dbar/2+dcorn_2)/rcorn);

-- screw bar

PHISCR = 45.00;		phiscr = PHISCR*deg;
DSCR = 16.00;		dscr = DSCR*mm*shrink;
HSCR = 17.00;		hscr = HSCR*mm*shrink;
psiscr = Asin((dscr/2)/ryok);

-- area of filling factor 1/2 / mesh-aid keypoints

YAR05 = 220.00;		yar05 = YAR05*mm*shrink;
xar05 = Sqrt(rcorn*rcorn-yar05*yar05);

h = 1.0*mm*shrink;
d = 5.00*mm*shrink;
xar05h_1 = xar05;
yar05h_1 = yar05-h;
xar05h_2 = xar05-d;
yar05h_2 = yar05;

-- holes

YH1 = 180.00;		yh1 = YH1*mm*shrink;
RH1 = 30.00;		rh1 = RH1*mm*shrink;
XH2 = 90.00;		xh2 = XH2*mm*shrink;
YH2 = 150.00;		yh2 = YH2*mm*shrink;
RH2 = 10.25;		rh2 = RH2*mm*shrink;
XH3 = 125.00;		xh3 = XH3*mm*shrink;
YH3 = 125.00;		yh3 = YH3*mm*shrink;
RH3 = 6.1;		rh3 = RH3*mm*shrink;



-- COLLAR SPECIFIC VARIABLES



-- UPPER STRUCTURE (us)

USR = 87.00;		usr = USR*mm*cshrink;
USBH1 = 8.5;		usbh1 = USBH1*mm*cshrink;
USBH2 = 7.5;		usbh2 = USBH2*mm*cshrink;
USBW = 2.5;		usbw = USBW*mm*cshrink;
USPHI1 = 25.00;		usphi1 = USPHI1*deg;
USPHI2 = 65.00;		usphi2 = USPHI2*deg;
USB1D = 4.65;		usb1d = USB1D*mm*cshrink;
USFLATY = 86.05;	usflaty = USFLATY*mm*cshrink;
USB2D = 3.00;		usb2d = USB2D*mm*cshrink;

usbs = Sqrt(usr*usr-usbw*usbw);

uspsi1 = Asin(usb1d/usr);

usflatx = Sqrt(usr*usr-usflaty*usflaty);


-- LOWER STRUCTURE (ls)

LSPOINT = 15.595;	lspoint = LSPOINT*mm*cshrink;
LSH = 28.00;		lsh = LSH*mm*cshrink;
LSPHI = 13.891;		lsphi = LSPHI*deg;
LSR = 59.995;		lsr = LSR*mm*cshrink;

-- intersection of circle(x^2+y^2 = r^2) and line(y=kx+d)

d = lspoint;
k = 1/Tan(lsphi);
a = (1+k*k);
b = 2*k*d;
c = d*d-lsr*lsr;
lsux = ((-1)*b+Sqrt(b*b-4*a*c))/(2*a);
lsuy = Sqrt(lsr*lsr-lsux*lsux);

lsdx = (lsh-lspoint)*Tan(lsphi); 

lsux45 = lsux*(Sqrt(2)/2);
lsuy45 = lsuy*(Sqrt(2)/2);

ls2x = lsuy45+lsux45;
ls2y = lsuy45-lsux45;
ls5x = lsuy45-lsux45;
ls5y = lsuy45+lsux45;

lsh45 = lsh*(Sqrt(2)/2);
lsdx45 = lsdx*(Sqrt(2)/2);

ls3x = lsh45+lsdx45;
ls3y = lsh45-lsdx45;
ls4x = lsh45-lsdx45;
ls4y = lsh45+lsdx45;
