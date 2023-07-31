!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!      РАСЁТ PSF В ПЛОСКОСТИ ИЗОБРАЖЕНИЯ       !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CURRENT_ZEMAX_FILE$ = $CALLSTR(1)
RESULT_ZEMAX_FILE$  = $CALLSTR(2)
PREFIX$             = $CALLSTR(3)
POSTFIX$            = $CALLSTR(4)

!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ДЛЯ ОЦЕНКИ ВРЕМЕНИ РАСЧЕТА PSF
TIMER

OPEN RESULT_ZEMAX_FILE$ 
OUTPUT RESULT_ZEMAX_FILE$, APPEND
FORMAT .7 EXP

!! SAMPLING MAY BE 1 (32 X 32), 2 (64 X 64), 3 (128 X 128), ETC... UP TO 2048 X 2048
!! CURRENT VAL 1024 X 1024
PSF_SAMPLING     = CALD(1)

!! THE VECTOR ARGUMENT MUST BE AN INTEGER VALUE BETWEEN 1 AND 4, AND SPECIFIES WHICH
!! VECTOR ARRAY THE DATA SHOULD BE PLACED IN.
PSF_VECTOR       = CALD(2)

!! THE UNNORMALIZED FLAG IS ZERO IF THE DATA SHOULD BE NORMALIZED TO A PEAK OF 1.0, IF THE
!! UNNORMALIZED VALUE IS 1, THEN THE DATA IS RETURNED UNNORMALIZED.
PSF_UNNORMALIZED = CALD(3)

!! IF PHASE FLAG IS ZERO, THE DATA RETURNED IS INTENSITY,
!! IF 1, THEN THE PHASE IN DEGREES IS RETURNED
PSF_PHASE_FLAG   = CALD(4)

!! THE IMAGEDELTA VALUE IS THE SPACING BETWEEN PSF POINTS IN
!! MICROMETERS, USE ZERO FOR THE DEFAULT SPACING
PSF_IMG_DELTA    = CALD(5)

!! УСТАНОВКА РАЗМЕРА ВНУТРЕННЕГО БУФЕРА ДЛЯ ЗАПИСИ В НЕГО РЕЗУЛЬТАТА PSF
!! SETVECSIZE POWR(POWR(2, PSF_SAMPLING) * 32, 2) * 4
SETVECSIZE POWR(POWR(2, PSF_SAMPLING) * 32, 2) * 2	
COUNT = NFLD() * NWAV()
COUNER = 0
N_SURF = NSUR()
MAX_FIELD = MAXF()
PRINT PREFIX$
PRINT "  ", $QUOTE(), "PSF", $QUOTE(), ":["
FOR WAVE_ID = 1, NWAV(), 1
	FOR FIELD_ID = 1, NFLD(), 1
			  COUNER = COUNER + 1	
			  GETPSF WAVE_ID, FIELD_ID, PSF_SAMPLING, PSF_VECTOR, PSF_UNNORMALIZED, PSF_PHASE_FLAG, PSF_IMG_DELTA
			  if (vec1(0) == 0)
			  	PRINT "  {"	
			  	PRINT "    ",  $QUOTE(), "ERROR", $QUOTE(), ": ", $QUOTE(), "PSF Computation aborted.", $QUOTE()
				IF (COUNT != COUNER)
					PRINT "  },"
				ELSE
					PRINT "  }"
				ENDIF	
				GOTO 3
			  ENDIF
			  if (vec1(0) == -1) 
				PRINT "  {"	
				PRINT "    ", $QUOTE(), "ERROR", $QUOTE(), ": ", $QUOTE(), "SETVECSIZE too small for PSF data.", $QUOTE()
				IF (COUNT != COUNER)
					PRINT "  },"
				ELSE
					PRINT "  }"
				ENDIF	
			  	GOTO 3
			  ENDIF
			  if (vec1(0) == -2) 
				PRINT "  {"	
				PRINT "    ", $QUOTE(), "ERROR", $QUOTE(), ": ", $QUOTE(), "Not enough system RAM for PSF data.", $QUOTE()
				IF (COUNT != COUNER)
					PRINT "  },"
				ELSE
					PRINT "  }"
				ENDIF	
			  	GOTO 3
			  ENDIF
			  if (vec1(0) == -3)
				PRINT "  {"	
			  	PRINT "    ",  $QUOTE(), "ERROR", $QUOTE(), ": ", $QUOTE(), "Sampling to low. Data inaccurate.", $QUOTE()
				IF (COUNT != COUNER)
					PRINT "  },"
				ELSE
					PRINT "  }"
				ENDIF	
			  	GOTO 3
			  ENDIF
			  N_POINTS  = vec1(0)
			  PSF_DELTA = vec1(N_POINTS + 1)
			
			  HX = FLDX(FIELD_ID)/MAX_FIELD
			  HY = FLDY(FIELD_ID)/MAX_FIELD
			  RAYTRACE HX, HY, 0, 0, PWAV(WAVE_ID)
			  X_CHIEF = RAYX(N_SURF)
			  Y_CHIEF = RAYY(N_SURF)
			  PRINT "  {"
			  PRINT "    ", $QUOTE(), "FIELD_ID", $QUOTE(), " :", FIELD_ID,","
			  PRINT	"    ", $QUOTE(), "WAVE_ID", $QUOTE(), "  :", WAVE_ID ,","
			  PRINT	"    ", $QUOTE(), "CENTER", $QUOTE(), ":{", $QUOTE(), "X", $QUOTE(), ": ", X_CHIEF, ", ", $QUOTE(), "Y", $QUOTE(), ": ", Y_CHIEF,"},"
			  PRINT	"    ", $QUOTE(), "N_POINTS", $QUOTE(), " :", N_POINTS ,","
			  PRINT	"    ", $QUOTE(), "PSF_DELTA", $QUOTE(), ":", PSF_DELTA ,","
			  PRINT	"    ", $QUOTE(), "PSF_DATA", $QUOTE(), " : ["
			  PRINT	"     ",
			  FOR i = 1, N_POINTS - 1, 1
					PRINT $STR(vec1(i)) + ", ",
			  NEXT
			  PRINT vec1(N_POINTS) 
			  PRINT "    ]" 
  	          IF (COUNT != COUNER)
		      	PRINT "  },"
		      ELSE
		      	PRINT "  }"
		      ENDIF	
			  LABEL 3
	NEXT FIELD_ID
NEXT WAVE_ID
PRINT "  ]", POSTFIX$
CLOSE
!! ВЫВОД ВРЕМЕНИ РАСЧЁТА PSF В КОНСОЛЬ
OUTPUT SCREEN
PRINT "Scheme: ", CURRENT_ZEMAX_FILE$, " PSF elapsed time: ", ETIM(), " seconds"