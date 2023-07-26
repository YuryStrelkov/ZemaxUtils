!! SUSPENDUPDATES

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!   ВВОД ПУТИ К ФАЙЛУ СО СПИСКОМ ZEMAX СХЕМ    !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

SCHEMES_TASK_LIST$ = ""
INPUT "ENTER TASK FILE LOCATION:", SCHEMES_TASK_LIST$
IF(SLEN(SCHEMES_TASK_LIST$) == 0)THEN END
TMP$ = ""
FINDFILE TMP$, SCHEMES_TASK_LIST$

IF(SLEN(TMP$) == 0)
	PRINT "TASK LIST DOES NOT EXISTS AT PATH : '", SCHEMES_TASK_LIST$, "',"
	SCHEMES_TASK_LIST$ = "E:\Aist_T\ZemaxScript\TASK\SCHEMES_LIST.txt"
ENDIF

OUTPUT SCREEN

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!   Вывод информации о рассчётных вводных      !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PRINT "Schemes src file : ", SCHEMES_TASK_LIST$
!! PRINT "Schemes res file : ", SCHEMES_RESULT_FILE$

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!     ЗАГРУЗКА ВСЕХ ПУТЕЙ К  ZEMAX ФАЙЛАМ      !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ZEMAX_FILES$ = ""
ZEMAX_FILES_SETTINGS$ = "" 
ZEMAX_FILES_CNTR = 0
OPEN SCHEMES_TASK_LIST$

!! Чтение всех путей из файла SCHEMES_TASK_LIST$
LABEL 1
		READSTRING CURRENT_FILE_PATH$
		IF (EOFF()) THEN GOTO 2
		ZEMAX_FILES_CNTR = ZEMAX_FILES_CNTR + 1
		ZEMAX_FILES$ = ZEMAX_FILES$ + $GETSTRING(CURRENT_FILE_PATH$, 1) + " "
		
		ZEMAX_FILES_SETTINGS$ = ZEMAX_FILES_SETTINGS$ + $GETSTRING(CURRENT_FILE_PATH$, 2) + " "
		ZEMAX_FILES_SETTINGS$ = ZEMAX_FILES_SETTINGS$ + $GETSTRING(CURRENT_FILE_PATH$, 3) + " "
		ZEMAX_FILES_SETTINGS$ = ZEMAX_FILES_SETTINGS$ + $GETSTRING(CURRENT_FILE_PATH$, 4) + " "
		ZEMAX_FILES_SETTINGS$ = ZEMAX_FILES_SETTINGS$ + $GETSTRING(CURRENT_FILE_PATH$, 5) + " "
		GOTO 1
LABEL 2
CLOSE

IF (ZEMAX_FILES_CNTR == 0)
	PRINT "TASK FILE INCORRECT :", CURRENT_FILE_PATH$
	END
ENDIF

!! Вывод всех путей из файла SCHEMES_TASK_LIST$
PRINT "FILES FOUND IN TSAK : ", ZEMAX_FILES_CNTR 
FOR PATH_ID = 1, ZEMAX_FILES_CNTR, 1
	SS$ = $GETSTRING(ZEMAX_FILES$, PATH_ID)
	PRINT "File : ", SS$
NEXT PATH_ID
PRINT

TIME_TOTAL = 0.0

FOR ZEMAX_FILE_ID = 1, ZEMAX_FILES_CNTR, 1
	COMPUTE_COMMON$ =  $GETSTRING(ZEMAX_FILES_SETTINGS$, (ZEMAX_FILE_ID - 1) * 4 + 1)
	COMPUTE_SPOT$   =  $GETSTRING(ZEMAX_FILES_SETTINGS$, (ZEMAX_FILE_ID - 1) * 4 + 2)
	COMPUTE_MTF$    =  $GETSTRING(ZEMAX_FILES_SETTINGS$, (ZEMAX_FILE_ID - 1) * 4 + 3)
	COMPUTE_PSF$    =  $GETSTRING(ZEMAX_FILES_SETTINGS$, (ZEMAX_FILE_ID - 1) * 4 + 4)
	
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!                                              !!
	!!       ЗАГРУЗКА ТЕКУЩЕГО ZEMAX ФАЙЛА          !!
	!!                                              !!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	!! ТЕКУЩИЙ ZEMAX ФАЙЛ
	CURRENT_ZEMAX_FILE$ = $GETSTRING(ZEMAX_FILES$, ZEMAX_FILE_ID)

	CALLSETSTR 1, CURRENT_ZEMAX_FILE$	
	CALLMACRO "COMPUTE_UTILS\PATH_UTILS.ZPL"
	
	F_DIR$  = $CALLSTR(1)
	F_NAME$ = $CALLSTR(2)
	F_EXT$  = $CALLSTR(3)
	
	SCHEMES_RESULT_FILE$ = F_DIR$ + "RESULTS\" + F_NAME$ + ".json"
	
	PRINT "COMPUTING FILE : ", SCHEMES_RESULT_FILE$
		
	CALLSETSTR 1, CURRENT_ZEMAX_FILE$
	CALLSETSTR 2, SCHEMES_RESULT_FILE$

	!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ВРЕМЕНИЯ РАСЧЁТА
	TIMER
	
	!! ЗАГРУЗКА ZEMAX СХЕМЫ
	LOADLENS CURRENT_ZEMAX_FILE$, 0, 1
	UPDATE ALL
	
	OPEN SCHEMES_RESULT_FILE$
	OUTPUT RESULT_ZEMAX_FILE$ 
	PRINT ""
	OUTPUT SCHEMES_RESULT_FILE$, APPEND
	PRINT "{"
	CLOSE
	OUTPUT SCREEN

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!                                              !!
	!!   ЗАПИСЬ ОСНОВНЫХ ПАРАМЕТРОВ ZEMAX ФАЙЛА     !!
	!!                                              !!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	IF (COMPUTE_COMMON$ $== "1")
		!! PREFIX
		CALLSETSTR 3, ""
		
		!! POSTFIX
		CALLSETSTR 4, ""
		IF (COMPUTE_SPOT$ $== "1") THEN CALLSETSTR 4, ","
		IF (COMPUTE_MTF$ $== "1") THEN CALLSETSTR 4, ","
		IF (COMPUTE_PSF$ $== "1") THEN CALLSETSTR 4, ","
		
		CALLSETDBL 1, 16
		
		CALLSETDBL 2, 16
		
		CALLMACRO "COMPUTE_UTILS\SCHEME_ARGS.ZPL"
	ENDIF
		
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!                                              !!
	!!  РАСЁТ SPOT-DIAGRAM В ПЛОСКОСТИ ИЗОБРАЖЕНИЯ  !!
	!!                                              !!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    IF (COMPUTE_SPOT$ $== "1")
		!! КОЛИЧЕСТВО ЛУЧЕЙ ДЛЯ РАСЧЁТА SPOT-DIAGRAM
		N_RAYS = 1024
		CALLSETDBL 1, N_RAYS

		!! PREFIX
		CALLSETSTR 3, ""

		!! POSTFIX
		CALLSETSTR 4, ""
		IF (COMPUTE_MTF$ $== "1") THEN CALLSETSTR 4, ","
		IF (COMPUTE_PSF$ $== "1") THEN CALLSETSTR 4, ","

		CALLMACRO "COMPUTE_UTILS\SCHEME_SPOTS.ZPL"
	ENDIF

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!                                              !!
	!!        РАСЧЕТ MTF ДЛЯ ТЕКУЩЕЙ СХЕМЫ          !!
	!!                                              !!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	IF (COMPUTE_MTF$ $== "1")
		!! НАЧАЛЬНАЯ ЧАСТОТА LINES PER MM
		FREQ_START = 0.01
		CALLSETDBL 1, FREQ_START
	
		!! КОНЕЧНАЯ ЧАСТОТА LINES PER MM
		FREQ_END   = 81.0
		CALLSETDBL 2, FREQ_END
	
		!! КОЛИЧЕСТВО ПРОМЕЖУТОЧНЫХ ЧАСТОТ
		NFREQ      =  81.0
		CALLSETDBL 3, NFREQ
	
		!! ШАГ ИЗМЕНЕНИЯ ЧАСТОТЫ
		DFREQ      = (FREQ_END - FREQ_START) / (NFREQ - 1)
		CALLSETDBL 4, DFREQ
		
		!! SAMPLING MAY BE 1 (32 X 32), 2 (64 X 64), 3 (128 X 128), ETC... UP TO 2048 X 2048
		MTF_SAMPLING   = 1
		CALLSETDBL 5, MTF_SAMPLING
	
		!! THE VECTOR ARGUMENT MUST BE AN INTEGER VALUE BETWEEN 1 AND 4,
		!! AND SPECIFIES WHICH VECTOR ARRAY THE DATA SHOULD BE PLACED IN.
		MTF_TYPE   = 1
		CALLSETDBL 6, MTF_TYPE 
	
		!! 1 FOR MTF, 2 FOR REAL PART, 3 FOR IMAGINARY PART,
		!! 4 FOR PHASE IN RADIANS, 5 FOR SQUARE WAVE MTF.
		MTF_VECTOR = 1 
		CALLSETDBL 7, MTF_VECTOR 
	
		!! PREFIX
		CALLSETSTR 3, ""
	
		!! POSTFIX
		CALLSETSTR 4, ""
		IF (COMPUTE_PSF$ $== "1") THEN CALLSETSTR 4, ","
		
		!! CALLMACRO "COMPUTE_UTILS\SCHEME_MTF.ZPL"
		CALLMACRO "COMPUTE_UTILS\COMPUTE_MTF.ZPL"
	ENDIF

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!                                              !!
	!!      РАСЁТ PSF В ПЛОСКОСТИ ИЗОБРАЖЕНИЯ       !!
	!!                                              !!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	IF (COMPUTE_PSF$ $== "1")
		!! SAMPLING MAY BE 1 (32 X 32), 2 (64 X 64), 3 (128 X 128), ETC... UP TO 2048 X 2048
		!! CURRENT VAL 1024 X 1024
		PSF_SAMPLING     = 3
		CALLSETDBL 1, PSF_SAMPLING
		
		!! THE VECTOR ARGUMENT MUST BE AN INTEGER VALUE BETWEEN 1 AND 4, AND SPECIFIES WHICH
		!! VECTOR ARRAY THE DATA SHOULD BE PLACED IN.
		PSF_VECTOR       = 1
		CALLSETDBL 2, PSF_VECTOR
		
		!! THE UNNORMALIZED FLAG IS ZERO IF THE DATA SHOULD BE NORMALIZED TO A PEAK OF 1.0, IF THE
		!! UNNORMALIZED VALUE IS 1, THEN THE DATA IS RETURNED UNNORMALIZED.
		PSF_UNNORMALIZED = 1 
		CALLSETDBL 3, PSF_UNNORMALIZED
		
		!! IF PHASE FLAG IS ZERO, THE DATA RETURNED IS INTENSITY,
		!! IF 1, THEN THE PHASE IN DEGREES IS RETURNED
		PSF_PHASE_FLAG   = 0 
		CALLSETDBL 4, PSF_PHASE_FLAG
		
		!! THE IMAGEDELTA VALUE IS THE SPACING BETWEEN PSF POINTS IN
		!! MICROMETERS, USE ZERO FOR THE DEFAULT SPACING
		PSF_IMG_DELTA    = 0.2
		CALLSETDBL 5, PSF_IMG_DELTA
		
		!! PREFIX
		CALLSETSTR 3, ""
		
		!! POSTFIX
		CALLSETSTR 4, ""
		
		CALLMACRO "COMPUTE_UTILS\SCHEME_PSF.ZPL"
	ENDIF

	OPEN SCHEMES_RESULT_FILE$ 
	OUTPUT SCHEMES_RESULT_FILE$, APPEND
	PRINT "}"
	CLOSE

	OUTPUT SCREEN
	PRINT "Scheme: ", CURRENT_ZEMAX_FILE$, " calulations is done..."
	PRINT "Total elapsed time : ",  ETIM()
	PRINT
	!! END
NEXT ZEMAX_FILE_ID
