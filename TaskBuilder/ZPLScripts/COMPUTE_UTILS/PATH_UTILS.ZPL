!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                                !!
!!      ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ     !!
!!      ДИЕРЕКТОРИИ, ИМЕНИ И РАСШИРЕНИЯ ФАЙЛА     !!
!!                                                !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! ПЕРЕДАЧА ВХОДНЫХ ДАННЫХ ЧЕРЕЗ БУФЕР $CALLSTR(1)!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PROCESS_LINE$ = $CALLSTR(1)

FILE_EXT$       = ""
FILE_NAME$      = ""
FILE_DIR$       = ""
SPACER_EXT_POS  = 0
SPACER_NAME_POS = 0

LABEL GET_FILE_EXT
FOR INDEX = 1, SLEN(PROCESS_LINE$), 1
	S_VAL$ = $RIGHTSTRING(PROCESS_LINE$,INDEX)
	S_VAL$ = $LEFTSTRING(S_VAL$, 1)
	if (S_VAL$ $== ".")
		SPACER_EXT_POS = INDEX - 1
		FILE_EXT$ = $RIGHTSTRING(PROCESS_LINE$, SPACER_EXT_POS)
		!! PRINT SPACER_EXT_POS
		GOTO GET_FILE_NAME
	ENDIF
NEXT INDEX

LABEL GET_FILE_NAME
FOR INDEX = 1, SLEN(PROCESS_LINE$), 1
	S_VAL$ = $RIGHTSTRING(PROCESS_LINE$,INDEX)
	S_VAL$ = $LEFTSTRING(S_VAL$, 1)
	if (S_VAL$ $== "\")
		SPACER_NAME_POS = INDEX - 1
		FILE_NAME$ = $RIGHTSTRING(PROCESS_LINE$, SPACER_NAME_POS)
		FILE_NAME$ = $LEFTSTRING(FILE_NAME$, SLEN(FILE_NAME$) - SLEN(FILE_EXT$) - 1)
		!! PRINT SPACER_NAME_POS
		GOTO GET_FILE_DIR
	ENDIF
NEXT INDEX

LABEL GET_FILE_DIR
FILE_DIR$ = $LEFTSTRING(PROCESS_LINE$, SLEN(PROCESS_LINE$) - SPACER_NAME_POS)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!     ПЕРЕДАЧА ВЫХОДНЫХ ДАННЫХ ЧЕРЕЗ БУФЕРЫ      !!
!!     $CALLSTR(1) ДЛЯ  ДИРЕКТОРИИ ФАЙЛА          !! 
!!     $CALLSTR(2) ДЛЯ  ИМЕНИ ФАЙЛА               !! 
!!     $CALLSTR(3) ДЛЯ  РАСШИРЕНИЯ ФАЙЛА          !! 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CALLSETSTR 1, FILE_DIR$
CALLSETSTR 2, FILE_NAME$
CALLSETSTR 3, FILE_EXT$


!! PRINT FILE_DIR$
!! PRINT FILE_NAME$
!! PRINT FILE_EXT$