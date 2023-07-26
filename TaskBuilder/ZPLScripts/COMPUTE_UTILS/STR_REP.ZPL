!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                                !!
!!      ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ЗАМЕНЫ        !!
!!      СИМВОЛА "\" НА "\\" В ПУТИ К ФАЙЛУ        !!
!!                                                !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! ПЕРЕДАЧА ВХОДНЫХ ДАННЫХ ЧЕРЕЗ БУФЕР $CALLSTR(1)!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

PROCESS_LINE$ = $CALLSTR(1)
!! EXAMPLE : PROCESS_LINE$ = "E:\Aist_T\ZemaxScript\TASK\SCHEMES_LIST.txt"
S_LEN = SLEN(PROCESS_LINE$)
NEW_LN$ = ""

PREV_SPACER = 0
FOR INDEX = 1, S_LEN, 1
	S_VAL$ = $LEFTSTRING(PROCESS_LINE$,INDEX)
	S_VAL$ = $RIGHTSTRING(S_VAL$,1)
	if (S_VAL$ $== "\")
		S_VAL$ = $LEFTSTRING (PROCESS_LINE$, INDEX - 1)
		S_VAL$ = $RIGHTSTRING(S_VAL$,     SLEN(S_VAL$) - PREV_SPACER)
		PREV_SPACER = INDEX
		NEW_LN$ = NEW_LN$ + S_VAL$+ "\\"
	ENDIF
NEXT INDEX

NEW_LN$ = NEW_LN$ + $RIGHTSTRING(PROCESS_LINE$, SLEN(PROCESS_LINE$) - PREV_SPACER)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!     ПЕРЕДАЧА ВЫХОДНЫХ ДАННЫХ ЧЕРЕЗ БУФЕР       !!
!!     $CALLSTR(5) ДЛЯ  ИЗМЕНЁННОЙ СТРОКИ         !! 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CALLSETSTR 5, NEW_LN$


