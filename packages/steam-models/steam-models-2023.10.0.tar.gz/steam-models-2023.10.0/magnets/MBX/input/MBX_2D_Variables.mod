-- include-file of the variables rhic arc dipole magnet//PCM


-- refering to :
-- Drawing 12010057

-- GENERAL VARIABLES

-- Per HAGEN shrink
dv DCONT=0.0;
-- mm      = 1;
cont = 1.0*(1-DCONT);
mm = 0.001*cont;

Pi      = 3.14159265;
deg     = Pi/180;


-- YOKE SPECIFIC VARIABLES

-- Yoke RADii
RADIN  = 59.69;        	radin = RADIN*mm;
RADOUT = 133.35;	radout = RADOUT*mm;


-- RECtangle for bus
RECDIS = 91.948;        recdis = RECDIS*mm;
RECHEI = 31.75;		rechei = RECHEI*mm;
RECWID = 31.75;		recwid = RECWID*mm;

-- HELIum passage
HELIX  = 65.532;	helix  = HELIX*mm;
HELIY  = 80.9244;	heliy  = HELIY*mm;
HELIDI = 30.1498;	helidi = HELIDI*mm;

-- SATuartion Hole
SATHX  = 61.0616;	sathx  = SATHX*mm;
SATHY  = 43.561;	sathy  = SATHY*mm;
SATHDI = 9.525;		sathdi = SATHDI*mm;

-- hole for shear PIN
PINX  = 85.725;		pinx  = PINX*mm;
PINY  = 26.9748;	piny  = PINY*mm;
PINDI = 12.42822;	pindi = PINDI*mm;


-- APerture NOtch
APNOW = 5.08;		apnow = APNOW*mm;
APNOH = 5.08;		apnoh = APNOH*mm;


-- KEY notch
KEYX = 123.444;		keyx = KEYX*mm;
KEYY = 6.1976;		keyy = KEYY*mm;
KEYH = 7.1882;		keyh = KEYH*mm;
KEYW = 124.206;		keyw = KEYW*mm;

-- HEATer
HEATAN = 20;		heatan = HEATAN*deg; 
HEATW  = 6.731;		heatw  = HEATW*mm;
HEATH  = 6.731;		heath  = HEATH*mm;
-- heath not veryfied in drawing!


-- SURvey notch
SURX  = 90.4748;	surx = SURX*mm;
SURY  = 90.4748;	sury = SURY*mm;

-- loading FLAT
FLATX = 105.41;		flatx  = FLATX*mm;
FLATY = 61.8998;	flaty  = FLATY*mm; 		
FLATW = 5.588;		flatw  = FLATW*mm;
FLATH = 6.731;		flath  = FLATH*mm;
FLATNY = 68.326;	flatny = FLATNY*mm;



