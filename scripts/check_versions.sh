#!/usr/bin/env bash
# Vérifie que les versions épinglées sont identiques dans toutes les branches chapN
# (pyproject.toml + uv.lock) et, en option, dans le repo d'examen.
#
# Usage :
#   scripts/check_versions.sh                        # compare origin/chap1..origin/chap5
#   REFS="chap1 chap2" scripts/check_versions.sh     # autres refs git
#   EXAM_PYPROJECT=../exam_Langchain/pyproject.toml scripts/check_versions.sh
set -euo pipefail

REFS=${REFS:-"origin/chap1 origin/chap2 origin/chap3 origin/chap4 origin/chap5"}
EXAM_PYPROJECT=${EXAM_PYPROJECT:-}

pins=$(mktemp)
trap 'rm -f "$pins"' EXIT

extract_pyproject() { grep -oE '"[A-Za-z0-9_.-]+==[^"]+"' | tr -d '"' | tr 'A-Z_' 'a-z-' | sed 's/==/ /'; }

extract_lock() {
  awk '/^\[\[package\]\]/{name=""} /^name = /{gsub(/"/,"",$3); name=$3} /^version = /{gsub(/"/,"",$3); if (name!="") print name, $3}'
}

for ref in $REFS; do
  git show "$ref:pyproject.toml" | extract_pyproject | sed "s|$| $ref:pyproject.toml|" >> "$pins"
  if git cat-file -e "$ref:uv.lock" 2>/dev/null; then
    git show "$ref:uv.lock" | extract_lock | grep -E '^(langchain|langgraph|langsmith)' | sed "s|$| $ref:uv.lock|" >> "$pins"
  else
    echo "ERREUR : uv.lock absent de $ref" >&2
    exit 1
  fi
done

if [[ -n "$EXAM_PYPROJECT" ]]; then
  extract_pyproject < "$EXAM_PYPROJECT" | sed "s|$| $EXAM_PYPROJECT|" >> "$pins"
fi

status=0
for pkg in $(cut -d' ' -f1 "$pins" | sort -u); do
  versions=$(awk -v p="$pkg" '$1==p {print $2}' "$pins" | sort -u)
  if [[ $(echo "$versions" | wc -l) -gt 1 ]]; then
    echo "ÉCART $pkg :"
    awk -v p="$pkg" '$1==p {print "  " $2 "  (" $3 ")"}' "$pins" | sort -u
    status=1
  fi
done

if [[ $status -eq 0 ]]; then
  echo "OK : $(cut -d' ' -f1 "$pins" | sort -u | wc -l) paquets, versions identiques sur : $REFS ${EXAM_PYPROJECT}"
fi
exit $status
