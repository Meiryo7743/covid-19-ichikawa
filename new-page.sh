#!/bin/bash

echo "Select the page type:"
select type in Articles Cards
do
    if [ "$type" = "Articles" ]; then
        DATE=$(TZ=UTC-9 date +"%Y%m%d%H%M%S")
        DST="articles/$DATE"
        break
    elif [ "$type" = "Cards" ]; then
        read -p "Type the card title:" DATA
        DST="cards/$DATA"
        break
    else
        continue
    fi
done

ARTICLE_JA="$DST/index.ja.md"
ARTICLE_EN="$DST/index.en.md"

hugo new $ARTICLE_JA
hugo new $ARTICLE_EN

code content/$ARTICLE_JA
