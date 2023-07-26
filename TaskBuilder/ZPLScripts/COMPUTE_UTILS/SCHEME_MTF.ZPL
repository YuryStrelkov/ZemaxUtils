!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!        РАСЧЕТ MTF ДЛЯ ТЕКУЩЕЙ СХЕМЫ          !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CURRENT_ZEMAX_FILE$ = $CALLSTR(1)
RESULT_ZEMAX_FILE$  = $CALLSTR(2)
PREFIX$             = $CALLSTR(3)
POSTFIX$            = $CALLSTR(4)

!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ДЛЯ ОЦЕНКИ ВРЕМЕНИ РАСЧЕТА MTF
TIMER

OPEN RESULT_ZEMAX_FILE$ 
OUTPUT RESULT_ZEMAX_FILE$, APPEND
FORMAT .7 EXP

!! НАЧАЛЬНАЯ ЧАСТОТА LINES PER MM
FREQ_START = 0.0
!! CALD(1)

!! КОНЕЧНАЯ ЧАСТОТА LINES PER MM
FREQ_END   = 81.0 
!! CALD(2)

!! КОЛИЧЕСТВО ПРОМЕЖУТОЧНЫХ ЧАСТОТ
N_FREQ      = 81.0 
!! CALD(3)

!! ШАГ ИЗМЕНЕНИЯ ЧАСТОТЫ
!!(FREQ_END - FREQ_START) / (NFREQ - 1)
D_FREQ      = 1
!!(FREQ_END - FREQ_START) / (NFREQ - 1)
!! CALD(4)

!! SAMPLING MAY BE 1 (32 X 32), 2 (64 X 64), 3 (128 X 128), ETC... UP TO 2048 X 2048
MTF_SAMPLING = 2
!! CALD(5)

!! THE VECTOR ARGUMENT MUST BE AN INTEGER VALUE BETWEEN 1 AND 4,
!! AND SPECIFIES WHICH VECTOR ARRAY THE DATA SHOULD BE PLACED IN.
MTF_TYPE   = 1
!! CALD(6) 

!! 1 FOR MTF, 2 FOR REAL PART, 3 FOR IMAGINARY PART,
!! 4 FOR PHASE IN RADIANS, 5 FOR SQUARE WAVE MTF.
MTF_VECTOR = 1
!! CALD(7) 

!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ДЛЯ ОЦЕНКИ ВРЕМЕНИ РАСЧЕТА MTF

PRINT PREFIX$
PRINT "  ", $QUOTE(), "MTF", $QUOTE(), ":["
COUNT = NFLD() * NWAV()
COUNER = 0
FOR WAVE_ID = 1, NWAV(), 1
	FOR FIELD_ID = 1, NFLD(), 1
		 PRINT "   {"
		 PRINT "   ", $QUOTE(), "FIELD_ID", $QUOTE(), ": ", FIELD_ID, ","
		 PRINT "   ", $QUOTE(), "WAVE_ID", $QUOTE(), ": ", WAVE_ID, ","
		 PRINT "   ", $QUOTE(), "MTF", $QUOTE(), ": ["
		 CURR_FREQ = FREQ_START
		 FOR FREQ_ID = 0, N_FREQ - 1, 10
			  GETMTF FREQ_ID, WAVE_ID, FIELD_ID, 2, 1, 1 
			  !! CURR_FREQ = CURR_FREQ + D_FREQ
			  PRINT "           {", $QUOTE(), "FREQ", $QUOTE(), ": ",  FREQ_ID,  ", ",
			  PRINT  "", $QUOTE(), "TAN", $QUOTE(), ": ", vec1(0), ", ",
			  PRINT  "", $QUOTE(), "SAG", $QUOTE(), ": ", vec1(1), "},"
		 NEXT FREQ_ID
		 GETMTF FREQ_END, WAVE_ID, FIELD_ID, 2, 1, 1 
		 PRINT "           {", $QUOTE(), "FREQ", $QUOTE(), ": ",  FREQ_END,  ", ",
		 PRINT  "", $QUOTE(), "TAN", $QUOTE(), ": ", vec1(0), ", ",
		 PRINT  "", $QUOTE(), "SAG", $QUOTE(), ": ", vec1(1), "}"
		 PRINT "          ]"
		 COUNER = COUNER + 1
  	     IF (COUNT != COUNER)
		 	PRINT "  },"
		 ELSE
		 	PRINT "  }"
		 ENDIF	 
	NEXT FIELD_ID
NEXT WAVE_ID
PRINT "  ]", POSTFIX$
CLOSE
!! ВЫВОД ВРЕМЕНИ РАСЧЁТА MTF В КОНСОЛЬ
OUTPUT SCREEN
PRINT "Scheme: ", CURRENT_ZEMAX_FILE$, " MTF elapsed time: ", ETIM(), " seconds"