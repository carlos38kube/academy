#!/usr/bin/env bash
# Comprueba que todos los enlaces locales a .html apuntan a archivos existentes
cd "$(dirname "$0")"
errores=0
for f in *.html; do
  for destino in $(grep -o 'href="[^"#?:]*\.html' "$f" | sed 's/href="//'); do
    if [ ! -f "$destino" ]; then
      echo "ROTO: $f -> $destino"
      errores=$((errores+1))
    fi
  done
done
if [ "$errores" -gt 0 ]; then
  echo "$errores enlaces rotos"
  exit 1
fi
echo "OK: sin enlaces rotos"
