#!/bin/sh
domain=new_resource
target=Resources_ja.po
xgettext -L Java --from-code=utf-8 -k_ -d "$domain" `find . -name '*.java' -print`
python i18n_update.py "$target" "$domain".po > new.po
mv new.po "$target"
rm -f "$domain".po
msgcat -p Resources_ja.po > Resources_ja.properties
