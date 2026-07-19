#!/bin/bash
# init-calendar.sh — ensure the content calendar exists.
# Used by the social-media skill. Idempotent.
#
# Usage: bash scripts/init-calendar.sh

set -euo pipefail

PLUGIN_ROOT="${CODEBUDDY_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
CALENDAR="$PLUGIN_ROOT/templates/content-calendar.md"

if [ ! -f "$CALENDAR" ]; then
  mkdir -p "$(dirname "$CALENDAR")"
  cat > "$CALENDAR" <<'EOF'
# Content Calendar

> Maintained by the `social-media` skill. Append-only.

| Date | Idea | Platforms | Tone | Status |
|---|---|---|---|---|
| _YYYY-MM-DD_ | _One-line idea summary_ | _FB, IG, YouTube, X, LinkedIn, Gmail_ | _professional / casual / promotional / educational_ | _drafted_ / _posted_ / _archived_ |

<!--
Append a new row each time /raihan-toolkit:social is run.
Keep the table chronological (newest at the bottom).
NO AI-GENERATION FOOTER in this file.
-->
EOF
  echo "created=$CALENDAR"
else
  echo "exists=$CALENDAR"
fi
