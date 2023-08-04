!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!   ЗАПИСЬ ОСНОВНЫХ ПАРАМЕТРОВ ZEMAX ФАЙЛА     !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! ТЕКУЩИЙ ZEMAX ФАЙЛ
CURRENT_ZEMAX_FILE$ = $CALLSTR(1)
RESULT_ZEMAX_FILE$  = $CALLSTR(2)
PREFIX$             = $CALLSTR(3)
POSTFIX$            = $CALLSTR(4)

OPEN RESULT_ZEMAX_FILE$
OUTPUT RESULT_ZEMAX_FILE$, APPEND
FORMAT .7 EXP

CALLMACRO "COMPUTE_UTILS\STR_REP.ZPL"

PRINT PREFIX$
PRINT "  ", $QUOTE(), "SCHEME", $QUOTE(), "     :", $QUOTE(), "", $CALLSTR(5), "", $QUOTE(), ","
PRINT "  ", $QUOTE(), "NWAV", $QUOTE(), "       :", NWAV(),","
PRINT "  ", $QUOTE(), "NFLD", $QUOTE(), "       :", NFLD(),","

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!         ОСНОВНЫЕ ФОКУСНЫЕ РАССТОЯНИЯ         !!
!!              И ПАРАМЕТРЫ СИСТЕМЫ             !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
GETSYSTEMDATA 1
PRINT "  ", $QUOTE(), "ENTRIES_COUNT", $QUOTE(), ":         ", VEC1(0), ","
PRINT "  ", $QUOTE(), "APERTURE_VALUE", $QUOTE(), ":        ", VEC1(1), ","
PRINT "  ", $QUOTE(), "APODIZATION_FACTOR", $QUOTE(), ":    ", VEC1(2), ","
PRINT "  ", $QUOTE(), "APODIZATION_TYPE", $QUOTE(), ":      ", VEC1(3), ","
PRINT "  ", $QUOTE(), "USE_ENV_DATA", $QUOTE(), ":          ", VEC1(4), ","
PRINT "  ", $QUOTE(), "TEMP_C", $QUOTE(), ":                ", VEC1(5), ","
PRINT "  ", $QUOTE(), "PRESSURE_ATM", $QUOTE(), ":          ", VEC1(6), ","
PRINT "  ", $QUOTE(), "EFL", $QUOTE(), ":                   ", VEC1(7), ","
PRINT "  ", $QUOTE(), "IMAGE_SPACE_F_DIV_#", $QUOTE(), ":   ", VEC1(8), ","
PRINT "  ", $QUOTE(), "OBJECT_SPACE_NA", $QUOTE(), ":       ", VEC1(9), ","
PRINT "  ", $QUOTE(), "WORKING_F_DIV_#", $QUOTE(), ":       ", VEC1(10), ","
PRINT "  ", $QUOTE(), "ENTRANCE_PUPIL_DIA", $QUOTE(), ":    ", VEC1(11), ","
PRINT "  ", $QUOTE(), "ENTRANCE_PUPIL_POS", $QUOTE(), ":    ", VEC1(12), ","
PRINT "  ", $QUOTE(), "EXIT_PUPIL_DIA", $QUOTE(), ":        ", VEC1(13), ","
PRINT "  ", $QUOTE(), "EXIT_PUPIL_POS", $QUOTE(), ":        ", VEC1(14), ","
PRINT "  ", $QUOTE(), "PARAX_IMAGE_HEIGHT", $QUOTE(), ":    ", VEC1(15), ","
PRINT "  ", $QUOTE(), "PARAX_MAGNIFICATION", $QUOTE(), ":   ", VEC1(16), ","
PRINT "  ", $QUOTE(), "ANGULAR_MAGNIFICATION", $QUOTE(), ": ", VEC1(17), ","
PRINT "  ", $QUOTE(), "TOTAL_TRACK", $QUOTE(), ":           ", VEC1(18), ","
PRINT "  ", $QUOTE(), "USE_RAY_AIMING", $QUOTE(), ":        ", VEC1(19), ","
PRINT "  ", $QUOTE(), "X_PUPIL_SHIFT", $QUOTE(), ":         ", VEC1(20), ","
PRINT "  ", $QUOTE(), "Y_PUPIL_SHIFT", $QUOTE(), ":         ", VEC1(21), ","
PRINT "  ", $QUOTE(), "Z_PUPIL_SHIFT", $QUOTE(), ":         ", VEC1(22), ","
PRINT "  ", $QUOTE(), "STOP_SURFACE_NUMBER", $QUOTE(), ":   ", VEC1(23), ","

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!           ЗАПИСЬ ДЛИН ВОЛН В ФАЙЛ            !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PRINT "  ", $QUOTE(), "WAVELENGTHS", $QUOTE(), ":", "[",
	COUNT = NWAV() - 1
	if (COUNT < 1) THEN COUNT = 1
	FOR i = 1, COUNT, 1
		PRINT $STR(WAVL(i)) + ",",
	NEXT
	PRINT $STR(WAVL(NWAV())),
PRINT "],"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!       ЗАПИСЬ ВЕСОВ ДЛИН ВОЛН В ФАЙЛ          !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PRINT "  ", $QUOTE(), "WAVELENGTHS_WEIGHTS", $QUOTE(), ":", "[",
	COUNT = NWAV() - 1
	if (COUNT < 1) THEN COUNT = 1
	FOR i = 1, COUNT, 1
		PRINT $STR(WWGT(i)) + ",",
	NEXT
	PRINT $STR(WAVL(NWAV())),
PRINT "],"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!     ЗАПИСЬ ИНФОРМАЦИИ О ПОЛЯХ В ФАЙЛ         !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PRINT "  ", $QUOTE(), "FIELDS_TYPE", $QUOTE(), ": ", "", $QUOTE(), "ANGLE", $QUOTE(), ","
PRINT "  ", $QUOTE(), "FIELDS", $QUOTE(), ":", "["
	COUNT = NFLD() - 1
	if (COUNT < 1) THEN COUNT = 1
	FOR i = 1, COUNT, 1
		PRINT "    {", $QUOTE(), "FLDX", $QUOTE(), ": ", FLDX(i),
		PRINT ", ", $QUOTE(), "FLDY", $QUOTE(), ": ", FLDY(i),
		PRINT ", ", $QUOTE(), "FWGT", $QUOTE(), ": ", FWGT(i),
		PRINT ", ", $QUOTE(), "FVDX", $QUOTE(), ": ", FVDX(i),
		PRINT ", ", $QUOTE(), "FVDY", $QUOTE(), ": ", FVDY(i),
		PRINT ", ", $QUOTE(), "FVCX", $QUOTE(), ": ", FVCX(i),
		PRINT ", ", $QUOTE(), "FVCY", $QUOTE(), ": ", FVCY(i),
		PRINT ", ", $QUOTE(), "FVAN", $QUOTE(), ": ", FVAN(i),"},"
	NEXT
	PRINT "    {", $QUOTE(), "FLDX", $QUOTE(), ": ", FLDX(i),
	PRINT ", ", $QUOTE(), "FLDY", $QUOTE(), ": ", FLDY(i),
	PRINT ", ", $QUOTE(), "FWGT", $QUOTE(), ": ", FWGT(i),
	PRINT ", ", $QUOTE(), "FVDX", $QUOTE(), ": ", FVDX(i),
	PRINT ", ", $QUOTE(), "FVDY", $QUOTE(), ": ", FVDY(i),
	PRINT ", ", $QUOTE(), "FVCX", $QUOTE(), ": ", FVCX(i),
	PRINT ", ", $QUOTE(), "FVCY", $QUOTE(), ": ", FVCY(i),
	PRINT ", ", $QUOTE(), "FVAN", $QUOTE(), ": ", FVAN(i),"}"
PRINT "  ],"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!  РАСЁТ CHIEF-RAY В ПЛОСКОСТИ ИЗОБРАЖЕНИЯ     !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MAX_FIELD = MAXF()
!! PREVENT DIVIDE BY ZERO BUG
IF (MAX_FIELD == 0.0) THEN MAX_FIELD = 1.0,
N_SUR = NSUR()
COUNT = NFLD() * NWAV()
COUNER = 0
PRINT "  ", $QUOTE(), "CHIEF_RAY_CORDS", $QUOTE(), ": ["
FOR WAVE_ID = 1, NWAV(), 1
	FOR FIELD_ID = 1, NFLD(), 1
			hx = FLDX(FIELD_ID)/MAX_FIELD
			hy = FLDY(FIELD_ID)/MAX_FIELD
			RAYTRACE hx, hy, 0, 0, PWAV(WAVE_ID)
			PRINT "    {",
			PRINT "", $QUOTE(), "FIELD_ID", $QUOTE(), ": ", FIELD_ID, ",",
			PRINT "", $QUOTE(), "WAVE_ID", $QUOTE(), ": ", WAVE_ID, ",", 
			PRINT "", $QUOTE(), "POSITION", $QUOTE(), ": ",
			PRINT "{", $QUOTE(), "X", $QUOTE(), " : ", RAYX(N_SUR), ", ",
			PRINT "", $QUOTE(), "Y", $QUOTE(), " : ", RAYY(N_SUR),"}",
			COUNER = COUNER + 1
			if (COUNT != COUNER)THEN PRINT "},"
			if (COUNT == COUNER)THEN PRINT "}"
	NEXT FIELD_ID
NEXT WAVE_ID
PRINT "  ],"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!РАСЁТ CHIEF-RAY ДЛЯ РАЗНОГО ЗНАЧЕНИЯ УГЛА ПОЛЯ!!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!! ИЩЕМ ГРАНИЦЫ ПОЛЯ ПО УГЛУ - ОТ МИНИМАЛЬНОГО К 
!! МАКСИМАЛЬНОМУ ДЛЯ X И Y
HX_MAX = -1E32
HX_MIN =  1E32
HY_MAX = -1E32
HY_MIN =  1E32

FOR FIELD_ID = 1, NFLD(), 1
    HX = FLDX(FIELD_ID)
	HY = FLDY(FIELD_ID)
	IF (HX_MAX < HX) THEN HX_MAX = HX 
	IF (HX_MIN > HX) THEN HX_MIN = HX 
	IF (HY_MAX < HY) THEN HY_MAX = HY 
	IF (HY_MIN > HY) THEN HY_MIN = HY
NEXT FIELD_ID	


!! ЧИТАЕМ КОЛИЧЕСТВО ТОЧЕК ПО X И Y 
N_X_ANGLE_STEPS = 16 # CALD(1)
N_Y_ANGLE_STEPS = 16 # CALD(2)

!! PREVENT DIVIDE BY ZERO BUG
IF (N_X_ANGLE_STEPS <= 1.0) THEN N_X_ANGLE_STEPS = 16
IF (N_Y_ANGLE_STEPS <= 1.0) THEN N_Y_ANGLE_STEPS = 16

D_X_ANGLE = (HX_MAX - HX_MIN) / (N_X_ANGLE_STEPS - 1.0)
D_Y_ANGLE = (HY_MAX - HY_MIN) / (N_Y_ANGLE_STEPS - 1.0)

COUNT = N_X_ANGLE_STEPS * N_Y_ANGLE_STEPS

PRINT "  ", $QUOTE(), "RAY_CORDS_FIELD", $QUOTE(), ":"
PRINT "  ["

MAX_FIELD = MAXF()

FOR WAVE_ID = 1, NWAV(), 1
	PRINT "    {"
	PRINT "    ", $QUOTE(), "AX_MIN", $QUOTE(), "     : ", HX_MIN, ","
	PRINT "    ", $QUOTE(), "AX_MAX", $QUOTE(), "     : ", HX_MAX, "," 
	PRINT "    ", $QUOTE(), "AY_MIN", $QUOTE(), "     : ", HY_MIN, ","
	PRINT "    ", $QUOTE(), "AY_MAX", $QUOTE(), "     : ", HY_MAX, "," 
	PRINT "    ", $QUOTE(), "N_ANGLES_X", $QUOTE(), " : ", N_X_ANGLE_STEPS, ","
	PRINT "    ", $QUOTE(), "N_ANGLES_Y", $QUOTE(), " : ", N_Y_ANGLE_STEPS, "," 
	PRINT "    ", $QUOTE(), "WAVE_ID", $QUOTE(), "    : ", WAVE_ID , ","
	PRINT "    ", $QUOTE(), "POS_PER_ANG", $QUOTE(), ": ["
	COUNER = 0
	AY = HY_MIN
	FOR ANGLE_Y_ID = 1, N_Y_ANGLE_STEPS, 1
		AX = HX_MIN
		FOR ANGLE_X_ID = 1, N_X_ANGLE_STEPS, 1
			hx = AX / MAX_FIELD
			hy = AY / MAX_FIELD
			RAYTRACE hx, hy, 0, 0, PWAV(WAVE_ID)
			PRINT "      {",
			PRINT "", $QUOTE(), "AX", $QUOTE(), " : ", AX, ", ",
			PRINT "", $QUOTE(), "AY", $QUOTE(), " : ", AY, ", ",
			PRINT "", $QUOTE(), "X",  $QUOTE(), " : ", RAYX(N_SUR), ", ",
			PRINT "", $QUOTE(), "Y",  $QUOTE(), " : ", RAYY(N_SUR),		
			COUNER = COUNER + 1
			IF (COUNT != COUNER)
				PRINT "},"
			ELSE
				PRINT "}"
				PRINT "      ]"
			ENDIF
			AX = AX + D_X_ANGLE
		NEXT ANGLE_X_ID
		AY = AY + D_Y_ANGLE
	NEXT ANGLE_Y_ID
	IF (WAVE_ID != NWAV())
		PRINT "    },"
	ELSE
		PRINT "    }"
	ENDIF
NEXT WAVE_ID
PRINT "  ],"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!                ВЕНЬЕТИРОВНИЕ                 !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

PRINT "  ", $QUOTE(), "RAY_VIGNETTING", $QUOTE(), ":"
PRINT "  ["
FOR WAVE_ID = 1, NWAV(), 1
	PRINT "    {"
	PRINT "    ", $QUOTE(), "PX_MIN", $QUOTE(), "     : ", -1.0, ","
	PRINT "    ", $QUOTE(), "PX_MAX", $QUOTE(), "     : ",  1.0, "," 
	PRINT "    ", $QUOTE(), "PY_MIN", $QUOTE(), "     : ", -1.0, ","
	PRINT "    ", $QUOTE(), "PY_MAX", $QUOTE(), "     : ",  1.0, "," 
	PRINT "    ", $QUOTE(), "N_X", $QUOTE(), "        : ", N_X_ANGLE_STEPS, ","
	PRINT "    ", $QUOTE(), "N_Y", $QUOTE(), "        : ", N_Y_ANGLE_STEPS, "," 
	PRINT "    ", $QUOTE(), "WAVE_ID", $QUOTE(), "    : ", WAVE_ID , ","
	PRINT "    ", $QUOTE(), "VIG_PER_POS", $QUOTE(), ": ["
	COUNER = 0
	PUPIL_SIZE = 0.9
	PY = -PUPIL_SIZE
	D_X_ANGLE = 2.0 * PUPIL_SIZE / (N_Y_ANGLE_STEPS - 1)
	D_Y_ANGLE = 2.0 * PUPIL_SIZE / (N_X_ANGLE_STEPS - 1)
	FOR ANGLE_Y_ID = 1, N_Y_ANGLE_STEPS, 1
		PX = -PUPIL_SIZE
		FOR ANGLE_X_ID = 1, N_X_ANGLE_STEPS, 1
			RAYTRACE 0, 0, PX, PY,  PWAV(WAVE_ID)
			PRINT "      {",
			PRINT "", $QUOTE(), "PX", $QUOTE(), "   : ", PX, ",",
			PRINT "", $QUOTE(), "PY", $QUOTE(), "   : ", PY, ",",
			PRINT "", $QUOTE(), "X",  $QUOTE(), "   : ", RAYX(N_SUR), ",",
			PRINT "", $QUOTE(), "Y",  $QUOTE(), "   : ", RAYY(N_SUR), ",",
			PRINT "", $QUOTE(), "RAY_V", $QUOTE(), ": ", RAYV(), 			
			COUNER = COUNER + 1
			IF (COUNT != COUNER)
				PRINT "},"
			ELSE
				PRINT "}"
				PRINT "      ]"
			ENDIF
			PX = PX + D_X_ANGLE
		NEXT ANGLE_X_ID
		PY = PY + D_Y_ANGLE
	NEXT ANGLE_Y_ID
	IF (WAVE_ID != NWAV())
		PRINT "    },"
	ELSE
		PRINT "    }"
	ENDIF
NEXT WAVE_ID
PRINT "  ],"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!                 ПРОПУСКАНИЕ                  !!
!!                И ПОЛЯРИЗАЦИЯ                 !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

POLDEFINE 0, 1, 0, 0
PRINT "  ", $QUOTE(), "RAY_POL_FIELD", $QUOTE(), ":"
PRINT "  ["

MAX_FIELD = MAXF()
D_X_ANGLE = (HX_MAX - HX_MIN) / (N_X_ANGLE_STEPS - 1.0)
D_Y_ANGLE = (HY_MAX - HY_MIN) / (N_Y_ANGLE_STEPS - 1.0)

FOR WAVE_ID = 1, NWAV(), 1
	PRINT "    {"
	PRINT "    ", $QUOTE(), "AX_MIN", $QUOTE(), "     : ", HX_MIN, ","
	PRINT "    ", $QUOTE(), "AX_MAX", $QUOTE(), "     : ", HX_MAX, "," 
	PRINT "    ", $QUOTE(), "AY_MIN", $QUOTE(), "     : ", HY_MIN, ","
	PRINT "    ", $QUOTE(), "AY_MAX", $QUOTE(), "     : ", HY_MAX, "," 
	PRINT "    ", $QUOTE(), "N_ANGLES_X", $QUOTE(), " : ", N_X_ANGLE_STEPS, ","
	PRINT "    ", $QUOTE(), "N_ANGLES_Y", $QUOTE(), " : ", N_Y_ANGLE_STEPS, "," 
	PRINT "    ", $QUOTE(), "WAVE_ID", $QUOTE(), "    : ", WAVE_ID , ","
	PRINT "    ", $QUOTE(), "POL_PER_ANG", $QUOTE(), ": ["
	COUNER = 0
	AY = HY_MIN
	FOR ANGLE_Y_ID = 1, N_Y_ANGLE_STEPS, 1
		AX = HX_MIN
		FOR ANGLE_X_ID = 1, N_X_ANGLE_STEPS, 1
			hx = AX/MAX_FIELD
			hy = AY/MAX_FIELD
			!! RAYTRACE hx, hy, 0, 0, PWAV(WAVE_ID)
			POLTRACE hx, hy, 0, 0, PWAV(WAVE_ID), 2, nsur()
			PRINT "      {"
			PRINT "       ", $QUOTE(), "INTENSITY", $QUOTE(), "         : ", vec2(1), "," 
			PRINT "       ", $QUOTE(), "E_REAL", $QUOTE(), "            : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(2), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(3), ",",
			PRINT           $QUOTE(), "Z", $QUOTE(), ": ", vec2(4), "},"
			!!  
			PRINT "       ", $QUOTE(), "E_IMAG", $QUOTE(), "            : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(5), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(6), ",",
			PRINT           $QUOTE(), "Z", $QUOTE(), ": ", vec2(7), "},"
			!!  
			PRINT "       ", $QUOTE(), "S_REFLECTION", $QUOTE(), "      : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(8), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(9), "},"
			!! 
			PRINT "       ", $QUOTE(), "S_TRANSMISSION", $QUOTE(), "    : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(10), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(11), "},"
			!! 
			PRINT "       ", $QUOTE(), "P_REFLECTION", $QUOTE(), "      : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(12), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(13), "},"
			!! 
			PRINT "       ", $QUOTE(), "P_TRANSMISSION", $QUOTE(), "    : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(14), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(15), "},"
			!!  
			PRINT "       ", $QUOTE(), "PHASE", $QUOTE(), "             : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(16), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(17), ",",
			PRINT           $QUOTE(), "Z", $QUOTE(), ": ", vec2(18), "},"
			!!  
			PRINT "       ", $QUOTE(), "POL_ELLIPSE", $QUOTE(), "       : {",
			PRINT           $QUOTE(), "MAJOR_AXIS", $QUOTE(), ": ", vec2(19), ",",
			PRINT           $QUOTE(), "MINOR_AXIS", $QUOTE(), ": ", vec2(20), ",",
			PRINT           $QUOTE(), "ANGLE", $QUOTE(), ": ", vec2(21), "},"
			!!  
			PRINT "       ", $QUOTE(), "S_AMP_REFLECTION", $QUOTE(), "  : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(23), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(24), "},"
			!! 
			PRINT "       ", $QUOTE(), "S_AMP_TRANSMISSION", $QUOTE(), ": {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(25), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(26), "},"
			!!  
			PRINT "       ", $QUOTE(), "P_AMP_REFLECTION", $QUOTE(), "  : {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(27), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(28), "},"
			!! 
			PRINT "       ", $QUOTE(), "P_AMP_TRANSMISSION", $QUOTE(), ": {",
			PRINT           $QUOTE(), "X", $QUOTE(), ": ", vec2(29), ",",
			PRINT           $QUOTE(), "Y", $QUOTE(), ": ", vec2(30), "}"
			COUNER = COUNER + 1
			IF (COUNT != COUNER)
				PRINT "      },"
			ELSE
				PRINT "      }"
				PRINT "      ]"
			ENDIF
			AX = AX + D_X_ANGLE
		NEXT ANGLE_X_ID
		AY = AY + D_Y_ANGLE
	NEXT ANGLE_Y_ID
	IF (WAVE_ID != NWAV())
		PRINT "    },"
	ELSE
		PRINT "    }"
	ENDIF
NEXT WAVE_ID

PRINT "  ]", POSTFIX$
CLOSE