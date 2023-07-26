!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!  РАСЁТ SPOT-DIAGRAM В ПЛОСКОСТИ ИЗОБРАЖЕНИЯ  !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CURRENT_ZEMAX_FILE$ = $CALLSTR(1)
RESULT_ZEMAX_FILE$  = $CALLSTR(2)
PREFIX$             = $CALLSTR(3)
POSTFIX$            = $CALLSTR(4)

!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ДЛЯ ОЦЕНКИ ВРЕМЕНИ РАСЧЕТА
!! SPOT-DIAGRAM
TIMER
OPEN RESULT_ZEMAX_FILE$ 
OUTPUT RESULT_ZEMAX_FILE$, APPEND
FORMAT .7 EXP

MAX_FIELD = MAXF()
!! КОЛИЧЕСТВО ЛУЧЕЙ ДЛЯ РАСЧЁТА SPOT-DIAGRAM
N_RAYS = CALD(1) 
TWO_PI = 6.283185
N_SURF = NSUR()
!! СКО РАДИУС И ГЕОМЕТРИЧЕСКИЙ РАДИУС
R_RMS = 0.0 
R_GEO = 0.0 
!! КООРДИНАТЫ ЗРАЧКА
HX = 0.0
HY = 0.0
!! КООРДИНАТЫ ИЗОБОРАЖЕНИЯ
X_CHIEF = 0.0
Y_CHIEF = 0.0
COUNT = NFLD() * NWAV()
COUNER = 0

!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ДЛЯ ОЦЕНКИ ВРЕМЕНИ РАСЧЕТА MTF
TIMER
PRINT PREFIX$ 
PRINT "  ", $QUOTE(), "SPOT", $QUOTE(), ": ["
FOR FIELD_ID = 1, NFLD(), 1
	FOR WAVE_ID = 1, NWAV(), 1
			COUNER = COUNER + 1
			R_RMS  = 0.0 
			R_GEO  = 0.0
			WR_RMS = 0.0
			WR_GEO = 0.0
			HX = FLDX(FIELD_ID)/MAX_FIELD
			HY = FLDY(FIELD_ID)/MAX_FIELD
			RAYTRACE HX, HY, 0, 0, PWAV(WAVE_ID)
			X_CHIEF = RAYX(N_SURF)
			Y_CHIEF = RAYY(N_SURF)
			PRINT "  {"
			PRINT "    ", $QUOTE(), "FIELD_ID", $QUOTE(), ": ", FIELD_ID , ","
			PRINT "    ", $QUOTE(), "WAVE_ID", $QUOTE(), ": ", WAVE_ID, "," 
			PRINT "    ", $QUOTE(), "POINTS", $QUOTE(), ": ["
			FOR RAY_ID = 1, N_RAYS, 1
				angle = TWO_PI * RAND(1.0)
				! SQRT yields uniform distribution in pupil
				radius = SQRT(RAND(1.0))
				
				PUPIL_X = radius * COSI(angle)
				PUPIL_Y = radius * SINE(angle)
			
				RAYTRACE HX, HY, PUPIL_X, PUPIL_Y, PWAV(WAVE_ID)
				
				X_IMAGE = RAYX(N_SURF)
				Y_IMAGE = RAYY(N_SURF)
				
				IF (RAY_ID == N_RAYS)
					PRINT "    {", $QUOTE(), "X", $QUOTE(), ": ", X_IMAGE, ", ", $QUOTE(), "Y", $QUOTE(), ": ", Y_IMAGE,"}"
				ELSE
					PRINT "    {", $QUOTE(), "X", $QUOTE(), ": ", X_IMAGE, ", ", $QUOTE(), "Y", $QUOTE(), ": ", Y_IMAGE,"},"
				ENDIF
				
				X_IMAGE = X_IMAGE - X_CHIEF 
				Y_IMAGE = Y_IMAGE - Y_CHIEF 
				
				X_IMAGE = X_IMAGE * X_IMAGE
				Y_IMAGE = Y_IMAGE * Y_IMAGE
				
				R_RMS = R_RMS + X_IMAGE + Y_IMAGE
				R_GEO = R_GEO + SQRT(X_IMAGE + Y_IMAGE)
			NEXT RAY_ID
		R_RMS = SQRT(R_RMS / N_RAYS)
		R_GEO = R_GEO / N_RAYS
		PRINT "    ],"
		PRINT "    ", $QUOTE(), "R_RMS", $QUOTE(), ": ", R_RMS , ","
		PRINT "    ", $QUOTE(), "R_GEO", $QUOTE(), ": ", R_GEO 
  	    IF (COUNT != COUNER)
			PRINT "  },"
		ELSE
			PRINT "  }"
		ENDIF
	NEXT WAVE_ID
NEXT FIELD_ID
PRINT "  ]", POSTFIX$
CLOSE

!! ВЫВОД ВРЕМЕНИ РАСЧЁТА SPOT DIAGRAM В КОНСОЛЬ
OUTPUT SCREEN
PRINT "Scheme: ", CURRENT_ZEMAX_FILE$, " SPOT diagramm elapsed time: ", ETIM(), " seconds"