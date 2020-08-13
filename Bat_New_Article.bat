@echo off

for /f %%a in ('wmic os get LocalDateTime ^| findstr \.') DO set LDT=%%a
set CUR_DATE=%LDT:~0,12%

set ARTICLE_JA=articles/%CUR_DATE%/index.ja.md
set ARTICLE_EN=articles/%CUR_DATE%/index.en.md

hugo new %ARTICLE_JA%
hugo new %ARTICLE_EN%

code content/%ARTICLE_JA%

exit
