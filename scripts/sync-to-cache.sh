#!/bin/bash
# sync-to-cache.sh — copy the plugin folder into the persistent CodeBuddy cache.
# After running this, register the plugin in installed_plugins.json and enable
# it in settings.json (see README.md → Persistent install).
#
# Usage: bash scripts/sync-to-cache.sh

set -euo pipefail

PLUGIN_ROOT="${CODEBUDDY_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
PLUGIN_NAME="raihan-toolkit"
VERSION="1.0.0"

if [ -z "${USERPROFILE:-}" ] && [ -z "${HOME:-}" ]; then
  echo "ERROR: neither USERPROFILE nor HOME is set; can't locate .codebuddy" >&2
  exit 1
fi

HOME_DIR="${USERPROFILE:-$HOME}"
DEST="$HOME_DIR/.codebuddy/plugins/cache/local/$PLUGIN_NAME/$VERSION"

echo "Source: $PLUGIN_ROOT"
echo "Dest:   $DEST"

mkdir -p "$DEST"

# rsync if available (fast + skips unchanged); otherwise cp -r.
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude '.git' --exclude 'node_modules' "$PLUGIN_ROOT/" "$DEST/"
else
  rm -rf "$DEST"
  mkdir -p "$DEST"
  cp -r "$PLUGIN_ROOT"/. "$DEST"/
fi

echo
echo "Synced. Next steps:"
echo "  1. Add to $HOME_DIR/.codebuddy/installed_plugins.json:"
echo '     "'"$PLUGIN_NAME"'@local": [{ "scope":"user", "installPath":"'"${DEST//\\/\\\\}"'", "version":"'"$VERSION"'", "installedAt":"'$(date -Iseconds)'", "lastUpdated":"'$(date -Iseconds)'" }]'
echo "  2. Add to settings.json enabledPlugins:"
echo '     "'"$PLUGIN_NAME"'@local": true'
echo "  3. Restart cc to load."
