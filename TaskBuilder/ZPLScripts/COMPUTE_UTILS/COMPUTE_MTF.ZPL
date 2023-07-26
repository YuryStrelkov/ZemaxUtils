!! Mtf
!! ИНИЦИАЛИЗАЦИЯ ТАЙМЕРА ДЛЯ ОЦЕНКИ ВРЕМЕНИ РАСЧЕТА MTF
TIMER

TMP_MTF_FILE$ = $TEMPFILENAME()
GETTEXTFILE TMP_MTF_FILE$, Mtf

!! PRINT TMP_MTF_FILE$
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                              !!
!!        РАСЧЕТ MTF ДЛЯ ТЕКУЩЕЙ СХЕМЫ          !!
!!                                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CURRENT_ZEMAX_FILE$ = $CALLSTR(1)
RESULT_ZEMAX_FILE$  = $CALLSTR(2)
PREFIX$             = $CALLSTR(3)
POSTFIX$            = $CALLSTR(4)

OPEN TMP_MTF_FILE$
OUTPUT RESULT_ZEMAX_FILE$, APPEND

PRINT PREFIX$
PRINT "  ", $QUOTE(), "MTF", $QUOTE(), ": ", $QUOTE(),
LABEL 1
		READSTRING LINE$
		IF (EOFF()) THEN GOTO 2
		IF (SLEN(LINE$) == 0) THEN GOTO 1
		PREF$ = $GETSTRING(LINE$, 1)
		IF (PREF$ $== "File") THEN GOTO 1
		PRINT "          ",
		PRINT $GETSTRING(LINE$, 1)," ",
		PRINT $GETSTRING(LINE$, 2)," ",
		PRINT $GETSTRING(LINE$, 3)," ",
		PRINT $GETSTRING(LINE$, 4)," ",
		PRINT $GETSTRING(LINE$, 5)," ",
		PRINT $GETSTRING(LINE$, 7)," ",
		PRINT $GETSTRING(LINE$, 8)," ", "\n",
		GOTO 1
LABEL 2
PRINT $QUOTE(), POSTFIX$
CLOSE
!! ВЫВОД ВРЕМЕНИ РАСЧЁТА MTF В КОНСОЛЬ
OUTPUT SCREEN
PRINT "Scheme: ", CURRENT_ZEMAX_FILE$, " MTF elapsed time: ", ETIM(), " seconds"