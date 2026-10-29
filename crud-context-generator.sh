#!/usr/bin/env bash
set -euo pipefail

out="tmp.txt"
with_database=false

for arg in "$@"; do
  case "$arg" in
    --with-database)
      with_database=true
      ;;
    *)
      printf 'Nieznany argument: %s\n' "$arg" >&2
      exit 1
      ;;
  esac
done

if [[ "$with_database" == true ]]; then
  tail -n +1 schema.sql
fi

printf '\n\n'

{
  find operations/user -type f -name '*.py' -exec tail -n +1 {} +
  find routes/user -type f -name '*.py' -exec tail -n +1 {} +
  find templates/admin/users -type f -name '*.html' -exec tail -n +1 {} +
}