@echo off

echo Dir name:
set NAME=
set /p NAME=

set ARTICLE_JA=cards/%NAME%/index.ja.md
set ARTICLE_EN=cards/%NAME%/index.en.md

hugo new %ARTICLE_JA%
hugo new %ARTICLE_EN%

code content/%ARTICLE_JA%

exit
