-- include-file of the variables from MQY quadrupole magnet/Bernhard Auchmann-03.08.00
-- referring to:
-- yoke			LHCMQY__0012|2
-- collar		LHCMQY__0018|2|A


-- GENERAL VARIABLES

mm=0.001;
Pi=3.14159265;
deg=Pi/180;
BEAMD = 97.00;       	beamd=BEAMD*mm;

-- Per HAGEN introduce design variables
-- cshrink = 0.9973;
-- shrink = 0.998;
dv DCONT = 0.0;
shrink = 1.0*(1-DCONT);
dv DCCONT = 0.0;
cshrink = 1.0*(1-DCCONT);

-- BEAMTUNNEL

RBT = 94.5;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
HBARBT = 9.50;		hbarbt = HBARBT*mm*shrink;
DBARBT = 3.50;		dbarbt = DBARBT*mm*shrink;


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

#dv YH1 = 107.46;	yh1 = YH1*mm*shrink;

#d0 = 6.1323*mm;		-- original min-distance between hole and beam tunnel
			-- (original situation: YH1=101, RH1=30)
#dv PAR = 0.9891;	-- 1 means min-distance d0, 0 means RH1=0 

#rh1 = PAR*(Sqrt(((yh1-Sqrt(2)*(rbt+hbarbt)+beamd)/2)*((yh1-Sqrt(2)*(rbt+hbarbt)+beamd)/2) + (yh1-((yh1+Sqrt(2)*(rbt+hbarbt)-beamd)/2))*(yh1-((yh1+Sqrt(2)*(rbt+hbarbt)-beamd)/2)))-d0);

YH1 = 101.00;		yh1 = YH1*mm*shrink;
RH1 = 30.00;		rh1 = RH1*mm*shrink;
XH2 = 86.5;		xh2 = XH2*mm*shrink;
YH2 = 143.00;		yh2 = YH2*mm*shrink;
RH2 = 13.00;		rh2 = RH2*mm*shrink;
XH3 = 140.00;		xh3 = XH3*mm*shrink;
YH3 = 120.00;		yh3 = YH3*mm*shrink;
RH3 = 6.1;		rh3 = RH3*mm*shrink;



-- COLLAR SPECIFIC VARIABLES


-- UPPER STRUCTURE (us)

USR = 93.00;		usr = USR*mm*cshrink;
USBH1 = 7.5;		usbh1 = USBH1*mm*cshrink;
USBH2 = 6.00;		usbh2 = USBH2*mm*cshrink;
USB1D = 5.15;		usb1d = USB1D*mm*cshrink;
USFLATY = 91.00;	usflaty = USFLATY*mm*cshrink;
USB2D = 3.50;		usb2d = USB2D*mm*cshrink;
USPHI1 = 20.00;		usphi1 = USPHI1*deg;
USPHI2 = 70.00;		usphi2 = USPHI2*deg;

usflatx = Sqrt(usr*usr-usflaty*usflaty);
uspsi = Asin(usb1d/usr);

-- LOWER STRUCTURE (ls)

LSHELP2 = 3.747;		lshelp2 = LSHELP2*mm*cshrink;
LSHELP3 = 20.58;	lshelp3 = LSHELP3*mm*cshrink;
LSPHI2 = 27.00;		lsphi2 = LSPHI2*deg;
LSPHI3 = 17.00;		lsphi3 = LSPHI3*deg;
LSR1 = 71.00;		lsr1 = LSR1*mm*cshrink;
LSR2 = 53.9;		lsr2 = LSR2*mm*cshrink;
LSR3 = 35.00;		lsr3 = LSR3*mm*cshrink;

lsrd2 = lsr2-lshelp2;
lsrd3 = lsr3-lshelp3;

-- intersection of circle(x^2+y^2 = r^2) and line(y=kx+d)

-- level 3
d3 = lshelp3;
k3 = 1/Tan(lsphi3);
a3 = (1+k3*k3);
b3 = 2*k3*d3;
c3 = d3*d3-lsr3*lsr3;
lsx3 = ((-1)*b3+Sqrt(b3*b3-4*a3*c3))/(2*a3);
lsy3 = Sqrt(lsr3*lsr3-lsx3*lsx3); 

lsx3_45 = lsx3*(Sqrt(2)/2);
lsy3_45 = lsy3*(Sqrt(2)/2);

ls5x = lsy3_45+lsx3_45;
ls5y = lsy3_45-lsx3_45;
ls6x = lsy3_45-lsx3_45;
ls6y = lsy3_45+lsx3_45;

-- level 23
d23 = lshelp3;
k23 = 1/Tan(lsphi3);
a23 = (1+k23*k23);
b23 = 2*k23*d23;
c23 = d23*d23-lsr2*lsr2;
lsx23 = ((-1)*b23+Sqrt(b23*b23-4*a23*c23))/(2*a23);
lsy23 = Sqrt(lsr2*lsr2-lsx23*lsx23); 

lsx23_45 = lsx23*(Sqrt(2)/2);
lsy23_45 = lsy23*(Sqrt(2)/2);

ls4x = lsy23_45+lsx23_45;
ls4y = lsy23_45-lsx23_45;
ls7x = lsy23_45-lsx23_45;
ls7y = lsy23_45+lsx23_45;

-- level2
d2 = lshelp2;
k2 = 1/Tan(lsphi2);
a2 = (1+k2*k2);
b2 = 2*k2*d2;
c2 = d2*d2-lsr2*lsr2;
lsx2 = ((-1)*b2+Sqrt(b2*b2-4*a2*c2))/(2*a2);
lsy2 = Sqrt(lsr2*lsr2-lsx2*lsx2); 

lsx2_45 = lsx2*(Sqrt(2)/2);
lsy2_45 = lsy2*(Sqrt(2)/2);

ls3x = lsy2_45+lsx2_45;
ls3y = lsy2_45-lsx2_45;
ls8x = lsy2_45-lsx2_45;
ls8y = lsy2_45+lsx2_45;

-- level21
d21 = lshelp2;
k21 = 1/Tan(lsphi2);
a21 = (1+k21*k21);
b21 = 2*k21*d21;
c21 = d21*d2-lsr1*lsr1;
lsx21 = ((-1)*b21+Sqrt(b21*b21-4*a21*c21))/(2*a21);
lsy21 = Sqrt(lsr1*lsr1-lsx21*lsx21); 

lsx21_45 = lsx21*(Sqrt(2)/2);
lsy21_45 = lsy21*(Sqrt(2)/2);

ls2x = lsy21_45+lsx21_45;
ls2y = lsy21_45-lsx21_45;
ls9x = lsy21_45-lsx21_45;
ls9y = lsy21_45+lsx21_45;
