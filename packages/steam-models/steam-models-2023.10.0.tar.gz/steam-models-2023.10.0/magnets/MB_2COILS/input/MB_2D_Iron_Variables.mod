-- include-file of the variables for modified MB dipole
-- Christine Voellinger,Martin Aleksa, Bernhard Auchmann - 31.08.2000 
-- Hole added by Martin Aleksa                           - 15.11.2000 
-- Correction of the Nose and Nick by Nikolai Schwerg    - 25.10.2004
-- Checked by Bernhard Auchmann and Per Hagen            - 31.03.2011


-- referring to: 
-- yoke			LHCMB__A0136|0|C
-- inner yoke		LHCMB__A0139|0|B
-- outer yoke		LHCMB__A0140|0|B
-- insert		LHCMB__A0148|1|E
-- collar		LHCMB__A0099|0|C
-- coil sheet		LHCMB__A0021|0|B (design study by Christine Voellinger, not production)

-- GENERAL VARIABLES

-- Design variables added by Per HAGEN (for easier to deal with warm measurements)
mm      = 0.001;
Pi      = 3.14159265;
deg     = Pi/180;
--shrink  = 0.998;			-- yoke/insert shrink
dv DCONT=0.0;
shrink=1.0*(1-DCONT);
--cshrink = 0.9973;			-- collar shrink
dv DCCONT=0.0;
cshrink=1.0*(1-DCCONT);
--csshrink = 0.996;			-- coil sheet shrink
dv DCSCONT=0.0;
csshrink=1.0*(1-DCSCONT);
BEAMD   = 97.00;	beamd=BEAMD*mm;

-- YOKE SPECIFIC VARIABLES


-- outer shape

dv RYOKE = 275.00;	ryoke = RYOKE*mm*shrink;	

dv ALEL1 = 83.1;	alel1 = ALEL1*mm*shrink;	
dv BLEL1 = 100.00;	blel1 = BLEL1*mm*shrink;
dv ALEL2 = 86.85;	alel2 = ALEL2*mm*shrink;
dv D1 = 17.8;		d1 = D1*mm*shrink;
dv D2 = 14.5;		d2 = D2*mm*shrink;

-- houd

dv HOUDW = 27.00;	houdw = HOUDW*mm*shrink;
dv HOUDH = 6.00;	houdh = HOUDH*mm*shrink; 
dv INSWI = 65.00;	inswi = INSWI*mm*shrink;	

houdsh = beamd-houdw-inswi;

-- nose
-- defining the given values from drawing:

-- ___o<------HX1------>       o : keypoint
--    /                :
--   /_____o<----HX2--->
--         /           : ^
--        /            : |
--       /             : HY
--      /______________o v
--                       ^
-- 		      | RNOSE
--
-- the variable PHINOSEU has been dumped!

dv RNOSE = 256;         rnose = RNOSE*mm*shrink;	
dv PHINOS = 77;         phinos = PHINOS*deg;
dv HX1 = 25.00;		hx1 = HX1*mm*shrink;	
dv HX2 = 19.04;		hx2 = HX2*mm*shrink;
dv HY  = 270.89-RNOSE;	hy  = HY*mm*shrink;


-- nick
-- Definitions from drawing:
-- Given are the Coordinates of the boar in the middle 
-- of the nick, the radius of the boar and the angle.

--           /
--         / 
--    /\   |
--  /   \  |
-- /      0<--- XNICK
--        ^
--        | YNICK 

XNICK = 202.95;		xnick = XNICK*mm*shrink;
YNICK = 342.00/2;		ynick = YNICK*mm*shrink;
PHINICK = 60;           phinick = PHINICK *deg;
RNICK = 3;              rnick = RNICK * mm *shrink;

-- the point in the corner of the nick is given by:
--   [xnick-rnick, ynick - c]
-- with c the hypothenuse of the triangle R,c, phinick/2:
--   c = rnick * Tan(beta)
-- beta the opposite angle
--   beta = 90 - phinick/2
kpTEST = [xnick-rnick, ynick - rnick * Tan((Pi-phinick)/2)];
-- The x-coorinate of this point gives with the circle
-- equation the coordinates of kpnick_2
--   kpnick_2 = [xnick-rnick, Sqrt(ryoke**2 - (xnick-rnick)**2)];

-- The coordinates of kpnick_1 are given by a line and the circle
-- by solving the equations:
--   y = m * x + n
--   y = Sqrt(R**2 - x**2)
-- With:
--   R = ryoke
--   m = 1/Tan(phinick)
nick_m = 1/Tan(phinick);
--   n = y0 - m * x0
nick_n = ynick - rnick * Tan((Pi-phinick)/2) - nick_m * (xnick-rnick);
--   with:
--     x0 = xnick-rnick
--     y0 = ynick - c
-- Equation:
--   x**2 + 2*m*n/(1+m**2) * x + (n**2 - R**2)/(1+m**2) == 0
-- Solution:
--   x = - p/2 +- Sqrt((p/2)**2-q)
--   with:
--     p = 2*m*n/(1+m**2)
nick_p = 2 * nick_n * nick_m / (1 + nick_m * nick_m);
--     q = (n**2 - R**2)/(1+m**2)
nick_q = (nick_n*nick_n - ryoke*ryoke)/ (1 + nick_m * nick_m);
--   The Solution with positive sign is used:
nick_x = -nick_p/2 + Sqrt((nick_p/2)*(nick_p/2)-nick_q);

-- busbar

BBR  = 244.00;		bbr  = BBR*mm;
BBW  = 51.00;		bbw  = BBW*mm;
PHIM = 53.6;		phim = PHIM*deg; 

bush   = Sqrt(ryoke*ryoke-bbw*bbw/4)-bbr;
gammah = Atan(bbw/(2*ryoke));

-- holes

-- middlepoints of holes
dv LH1X = 17.00;	lh1x = LH1X*mm;     
dv LH1Y = 90.00;	lh1y = LH1Y*mm;
dv LH2X = 57.00;	lh2x = LH2X*mm;     
dv LH2Y = 220.00;	lh2y = LH2Y*mm;
dv LH3X = 90.32;	lh3x = LH3X*mm;     
dv LH3Y = 176.00;	lh3y = LH3Y*mm;
dv LH4X = 180.2;	lh4x = LH4X*mm;     
dv LH4Y = 120.2;	lh4y = LH4Y*mm;
dv LHHX = 0.00;		lhhx = LHHX*mm;     
dv LHHY = 179.6;	lhhy = LHHY*mm;

-- radius of holes
dv LH1R = 2.5;		lh1r = LH1R*mm*shrink;
dv LH2R = 15.00;	lh2r = LH2R*mm*shrink;
dv LH3R = 8.8;		lh3r = LH3R*mm*shrink;
dv LH4R = 8.8;		lh4r = LH4R*mm*shrink;
dv LHHR = 30.00;	lhhr = LHHR*mm*shrink;

-- other parameters of holes
dv PHIHCO = 30.00;	phihco = PHIHCO*deg;
linsh1 = Sqrt(1-((houdw+houdsh-d1)/alel1)*((houdw+houdsh-d1)/alel1))*blel1;	-- point on ellipse


-- MODIFIED INSERT SPECIFIC VARIABLES

dv LH5X = 32.1;		lh5x = LH5X*mm*shrink;     
-- dv LH5DY = 22.7;
dv LH5R = 8.1;		lh5r = LH5R*mm*shrink;

dv LINSPHI = 9.00;	linsphi=LINSPHI*deg;  
dv LINSPARANG = 41.8;	linsparang=LINSPARANG*deg; 
dv LINSNH = 8.2;	linsnh=LINSNH*mm*shrink;
dv LINSCUT = 56.;	linscut = LINSCUT*mm*shrink;

linsh=blel1*Sin(linsparang)-linsnh;
linsw=beamd-d2-alel2*Cos(linsparang);

yinscut1 = Sqrt(1-((beamd-d2-linscut)/alel2)*((beamd-d2-linscut)/alel2))*blel1;	-- point on ellipse
yinscut2 = (beamd-houdw-linscut)*Tan(linsphi)+blel1+houdh;

linsh2 = Sqrt(1-((houdw+houdsh-d2)/alel2)*((houdw+houdsh-d2)/alel2))*blel1;

linsh=blel1*Sin(linsparang)-linsnh;

-- point on ellipse

du1a = (d2-beamd+lh5x);
du1b = alel2*alel2*alel2*alel2*(blel1*blel1-2*lh5r*lh5r);
du1 = -blel1*blel1*blel1*blel1*du1a*du1a-du1b;
du2 = alel2*alel2*blel1*blel1*(du1a*du1a-lh5r*lh5r);
du3a = (alel2*alel2*alel2*alel2-alel2*alel2*du1a*du1a+blel1*blel1*du1a*du1a);
du3 = du3a*du3a;
du4 = (alel2*alel2*alel2*alel2+alel2*alel2*du1a*du1a-blel1*blel1*du1a*du1a);
du5 = (alel2*alel2*(alel2-blel1)*(alel2+blel1));

-- du1 = -(blel1**4*(-beamd+d2+lh5x)**2)-alel2**4*(blel1**2-2*lh5r**2);
-- du2 = alel2**2*blel1**2*((-beamd+d2+lh5x)**2-lh5r**2);
-- du3 = (alel2**4-alel2**2*(-beamd+d2+lh5x)**2+blel1**2*(-beamd+d2+lh5x)**2)**2;
-- du4 = (alel2**4+alel2**2*(-beamd+d2+lh5x)**2-blel1**2*(-beamd+d2+lh5x)**2);
-- du5 = (alel2**2*(alel2-blel1)*(alel2+blel1));

dxvar=Sqrt((du1+du2+Sqrt(blel1*blel1*blel1*blel1*(du3-2*alel2*alel2*du4*lh5r*lh5r+alel2*alel2*alel2*alel2*lh5r*lh5r*lh5r*lh5r)))/du5)/Sqrt(2);

lh5y=(blel1*blel1*dxvar*(beamd-d2-lh5x))/(alel2*alel2*Sqrt(-dxvar*dxvar+lh5r*lh5r));

dyvar=Sqrt(lh5r*lh5r-dxvar*dxvar);

-- COLLAR SPECIFIC VARIABLES

-- outer shape

CUSH1 = 92.00;		cush1 = CUSH1*mm*cshrink;
CUSH2 = 47.5;		cush2 = CUSH2*mm*cshrink;
CN1X = 179.95;		cn1x = CN1X*mm*cshrink;

-- upper structure (us)

USHOUT = 92.00;		ushout = USHOUT*mm*cshrink;
USHIN = 93.1;		ushin = USHIN*mm*cshrink;
USHTOP = 98.9;		ushtop = USHTOP*mm*cshrink;
USPHI = 30.00;		usphi = USPHI*deg;
USDOUT = 52.00;		usdout = USDOUT*mm*cshrink;
USDIN = 21.00;		usdin = USDIN*mm*cshrink;


-- lower structure (ls)

LSR1 = 15.00;		lsr1 = LSR1*mm*cshrink;
LSR2 = 44.88;		lsr2 = LSR2*mm*cshrink;
LSR3 = 60.98;		lsr3 = LSR3*mm*cshrink;
LSPHI1 = 52.5;		lsphi1 = LSPHI1*deg;
LSPHI2 = 19.01;		lsphi2 = LSPHI2*deg;
LSPHI3 = 48.67;		lsphi3 = LSPHI3*deg;
LSHHELP1 = 12.44;	lshhelp1 = LSHHELP1*mm*cshrink;
LSHHELP2 = 13.2;	lshhelp2 = LSHHELP2*mm*cshrink;
LSHHELP3 = 18.12;	lshhelp3 = LSHHELP3*mm*cshrink;
LSHMID = 30.3;		lshmid = LSHMID*mm*cshrink;

delta = lshhelp2 - lshhelp1;
lsdI = delta*Cos(lsphi2) + Sqrt(delta*Cos(lsphi2)*delta*Cos(lsphi2) + lsr1*lsr1 - delta*delta);	-- Cosine-theorem

lsdIIa = lshhelp1*Cos(Pi-lsphi2) + Sqrt(lshhelp1*Cos(Pi-lsphi2)*lshhelp1*Cos(Pi-lsphi2) + lsr2*lsr2 -lshhelp1*lshhelp1);	-- Cosine-theorem

lsdIIb = lshhelp3*Cos(Pi-lsphi3) + Sqrt(lshhelp3*Cos(Pi-lsphi3)*lshhelp3*Cos(Pi-lsphi3) + lsr2*lsr2 -lshhelp3*lshhelp3);

lsdIII = lshhelp3*Cos(Pi-lsphi3) + Sqrt(lshhelp3*Cos(Pi-lsphi3)*lshhelp3*Cos(Pi-lsphi3) + lsr3*lsr3 -lshhelp3*lshhelp3);

-- arcs and holes

XARC1 = 178.00;		xarc1 = XARC1*mm*cshrink;
RARC1 = 7.01;		rarc1 = RARC1*mm; -- shrinked scale
RARC2 = 11.01;		rarc2 = RARC2*mm; -- shrinked scale

XHOLE1 = 156.00;	xhole1 = XHOLE1*mm*cshrink;
XHOLE2 = 39.00;		xhole2 = XHOLE2*mm*cshrink;
YHOLE = 57.00;		yhole = YHOLE*mm*cshrink;

DHOLE1 = 10.00;		dhole1 = DHOLE1*mm*cshrink;
DHOLE2 = 10.02;		dhole2 = DHOLE2*mm*cshrink;
rhole1 = dhole1/2;
rhole2 = dhole2/2;


-- COIL SHEET (cs) SPECIFIC VARIABLES

-- PARAMETER SETTING

ILALPHA = 23.00;	ilalpha = ILALPHA*deg;		-- parameter for cut off of cs
OLH = 13.00;		olh = OLH*mm*csshrink;		-- height parameter for cut off of cs
IRONALPHA = 20.00;	ironalpha = IRONALPHA*deg;	-- cut off angle for inner iron inlay

-- general

POLY = 0.5;		poly = POLY*mm*csshrink;	-- polyamid layer thickness
RCIN = 28.00;		rcin = RCIN*mm*csshrink;	-- inner radius of the coil
RCMID = 43.4;		rcmid = RCMID*mm*csshrink;	-- mid radius
RCOUT = 59.3;		rcout = RCOUT*mm*csshrink;	-- outer radius

-- inner layer (IL)

ILQH = 0.5;		ilqh = ILQH*mm*csshrink;	-- inner layer quensh heater thickness
ILCS = 0.5;		ilcs = ILCS*mm*csshrink;	-- inner layer coil sheet thickness
ILHELP = 5.69;		ilhelp = ILHELP*mm*csshrink;	-- construction help line (see drawings)
ILSHIM = 0.2;		ilshim = ILSHIM*mm*csshrink;	-- shim inner layer
ILPHI = 19.01;		ilphi = ILPHI*deg;		-- construction help angle (see drawings)

-- outer layer (OL)

OLQH = 0.2;		olqh = OLQH*mm*csshrink;	-- outer layer quensh heater  
OLSHIM = 0.8;		olshim = OLSHIM*mm*csshrink;	-- shim outer layer
OLCSIN = 0.5;		olcsin = OLCSIN*mm*csshrink;	-- outer layer inner coil sheet 
OLCSOUT = 0.5;		olcsout = OLCSOUT*mm*csshrink;	-- outer layer outer coil sheet 
OLHELP = 14.79;		olhelp = OLHELP*mm*csshrink;	-- construction help line (see drawings)
OLPHI = 48.67;		olphi = OLPHI*deg;		-- construction help angle (see drawings)

-- inner layer calculations

-- Cosine theorem
ang = Pi-ilphi;						
d = ilhelp;
r = rcin;

ilrh1 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

-- cosine theorem result + shifting in orthogonal direction
il1x = ilrh1*Sin(ilphi) - (ilqh+poly)*Cos(ilphi);	
il1y = ilhelp + ilrh1*Cos(ilphi) + (ilqh+poly)*Sin(ilphi);

il2x = ilrh1*Sin(ilphi) - (ilqh+poly+2*ilcs+ilshim)*Cos(ilphi);
il2y = ilhelp + ilrh1*Cos(ilphi) + (ilqh+poly+2*ilcs+ilshim)*Sin(ilphi);

ang = Pi-ilphi;
d = ilhelp + (ilqh+poly)/Sin(ilphi);
r = rcmid+ilqh+poly;

ilrh2 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

il3x = ilrh2*Sin(ilphi);
il3y = d + ilrh2*Cos(ilphi);

il7phi = Acos((d*d+r*r-ilrh2*ilrh2)/(2*r*d));

ang = Pi-ilphi;
d = ilhelp + (ilqh+poly+2*ilcs+ilshim)/Sin(ilphi);
r = rcmid+ilqh+poly+ilcs;

ilrh3 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

il4x = ilrh3*Sin(ilphi);
il4y = d + ilrh3*Cos(ilphi);

ang = Pi-(olphi-ilalpha);
d = olhelp;
r = rcmid+ilqh+poly;

ilrh4 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

il5x = ilrh4*Sin(olphi-ilalpha);
il5y = d + ilrh4*Cos(olphi-ilalpha);

il6phi = Acos((d*d+r*r-ilrh4*ilrh4)/(2*r*d));


-- outer layer calculations

ang = Pi-(olphi);
d = olhelp + (2*poly+olshim)/Sin(olphi);
r = rcmid+ilqh+poly+ilcs+olh;

olrh1 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

ol1x = olrh1*Sin(olphi);
ol1y = d + olrh1*Cos(olphi);

ang = Pi-(olphi);
d = olhelp + (2*poly+olshim)/Sin(olphi);
r = rcmid+ilqh+poly+ilcs+olh;

olrh2 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

ol2x = olrh2*Sin(olphi) - olcsout*Cos(olphi);
ol2y = d + olrh2*Cos(olphi) + olcsout*Sin(olphi);

ang = Pi-(olphi);
d = olhelp + (2*poly+olshim)/Sin(olphi);
r = rcout+olqh+poly;

olrh2 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

ol3x = olrh2*Sin(olphi);
ol3y = d + olrh2*Cos(olphi);

ol11phi = Acos((d*d+r*r-olrh2*olrh2)/(2*r*d));

ang = Pi-(olphi);
d = olhelp + (2*poly+olshim+olcsout)/Sin(olphi);
r = rcout+olqh+poly+olcsin+olcsout;

olrh3 = d*Cos(ang) + Sqrt(d*Cos(ang)*d*Cos(ang) + r*r - d*d);

ol4x = olrh3*Sin(olphi);
ol4y = d + olrh3*Cos(olphi);







