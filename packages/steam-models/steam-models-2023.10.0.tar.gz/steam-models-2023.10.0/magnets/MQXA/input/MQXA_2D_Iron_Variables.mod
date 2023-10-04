-- include-file of the variables from MQX quadrupole magnet/Bernhard Auchmann - 25.08.00

-- referring to: 
-- yoke		INSQ-M1_cross_section|A, KLHCIQ70M01-04-006
-- collar	KLHCIQ70M01-001


-- GENERAL VARIABLES

mm=0.001;
Pi=3.14159265;
deg=Pi/180;

-- Modified by Per Hagen Sep 2010 to use design variables
-- shrink = 0.998;
-- cshrink = 0.9973;
dv DCONT = 0.0;
shrink = 1.0*(1-DCONT);
dv DCCONT = 0.0;
cshrink = 1.0*(1-DCCONT);
-- shrink = 0.998;
-- cshrink = 0.9973;

--YOKE SPECIFIC VARIABLES


-- BEAMTUNNEL

RBT = 92.00;		rbt = RBT*mm*shrink;
PHIBT = 45.00;		phibt = PHIBT*deg;
PHIHATBT = 60.00;	phihatbt = PHIHATBT*deg;
RHATBT = 100.00;	rhatbt = RHATBT*mm*shrink;

-- yhatbt = -tan(phihatbt)*(xhatbt-rhatbt)
-- xhatbt*xhatbt + yhatbt*yhatbt = rbt*rbt

a = 1+1/((Tan(phihatbt))*(Tan(phihatbt)));
b = (-2)*rhatbt/Tan(phihatbt);
c = rhatbt*rhatbt-rbt*rbt;

xhatbt = ((-1)*b-Sqrt(b*b-4*a*c))/(2*a);

psihatbt = Asin(xhatbt/rbt);


-- OUTER FORM

ROUT = 235.00;		rout = ROUT*mm*shrink;
XCORN1 = 207.00;	xcorn1 = XCORN1*mm*shrink;
YCORN1 = 10.00;		ycorn1 = YCORN1*mm*shrink;
xbar1 = xcorn1;
YBAR1 = 50.00;		ybar1 = YBAR1*mm*shrink;
DBAR1 = 20.00;		dbar1 = DBAR1*mm*shrink;
XCORN2 = 170.00;	xcorn2 = XCORN2*mm*shrink;
YCORN2 = 130.00;	ycorn2 = YCORN2*mm*shrink;
XCORN3 = 130.00;	xcorn3 = XCORN3*mm*shrink;
YCORN3 = 170.00;	ycorn3 = YCORN3*mm*shrink;
D1BAR2 = 40.00;		d1bar2 = D1BAR2*mm*shrink;
D2BAR2 = 50.00;		d2bar2 = D2BAR2*mm*shrink;
H1BAR2 = 10.00;		h1bar2 = H1BAR2*mm*shrink;
H2BAR2 = 10.00;		h2bar2 = H2BAR2*mm*shrink;

BARW = 18.00;		barw = BARW*mm*shrink;

x2 = Sqrt(rout*rout - ycorn1*ycorn1);

x3 = Sqrt(rout*rout - (ybar1-dbar1/2)*(ybar1-dbar1/2));

x4 = Sqrt(rout*rout - (ybar1+dbar1/2)*(ybar1+dbar1/2));

x5 = Sqrt(rout*rout - ycorn2*ycorn2);

y6 = Sqrt(rout*rout - xcorn2*xcorn2);

x7 = Sqrt(rout*rout - ycorn3*ycorn3);

y8 = Sqrt(rout*rout - xcorn3*xcorn3);

y9 = Sqrt(rout*rout - (d1bar2/2)*(d1bar2/2));

-- HOLES

PHIH1 = 45.00;		phih1 = PHIH1*deg;
DH1 = 160.00;		dh1 = DH1*mm*shrink;
RH1 = 30.00;		rh1 = RH1*mm*shrink;

PHIH2 = 15.00;		phih2 = PHIH2*deg;
DH2 = 150.00;		dh2 = DH2*mm*shrink;
RH2 = 15.00;		rh2 = RH2*mm*shrink;



-- COLLAR SPECIFIC VARIABLES

-- UPPER STRUCTURE (us)

USR = 92.00;		usr = USR*mm*cshrink;
USARC = 88.9;		usarc = USARC*mm*cshrink;
USARCR = 3.00;		usarcr = USARCR*mm*cshrink;
USOUT = 96.00;		usout = USOUT*mm*cshrink;
USD1 = 4.928;		usd1 = USD1*mm*cshrink;
USD2 = 8.00;		usd2 = USD2*mm*cshrink;
USD3 = 1.774;		usd3 = USD3*mm*cshrink;
USD4 = 4.349;		usd4 = USD4*mm*cshrink;


-- LOWER STRUCTURE (ls)

LSHELP2 = 5.17;		lshelp2 = LSHELP2*mm*cshrink;	-- calculated with data of KLHCIQ70M01-07-01-001
LSHELP3 = 9.377;	lshelp3 = LSHELP3*mm*cshrink;	-- calculated with data of KLHCIQ70M01-07-01-00
LSPHI2 = 23.00;		lsphi2 = LSPHI2*deg;
LSPHI3 = 14.259;	lsphi3 = LSPHI3*deg;
LSR1 = 82.2;		lsr1 = LSR1*mm*cshrink;
LSR2 = 59.9;		lsr2 = LSR2*mm*cshrink;
LSR3 = 35.00;		lsr3 = LSR3*mm*cshrink;
LSR4 = 1.8;		lsr4 = LSR4*mm*cshrink;
LSHARC = 79.00;		lsharc = LSHARC*mm*cshrink;
LSHR = 3.00;		lshr = LSHR*mm*cshrink;
LSHPHI = 12.5;		lshphi = LSHPHI*deg;

lsrd2 = lsr2-lshelp2;
lsrd3 = lsr3-lshelp3;

yarc = Sqrt(lsr3*lsr3 - lsr4*lsr4);

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
