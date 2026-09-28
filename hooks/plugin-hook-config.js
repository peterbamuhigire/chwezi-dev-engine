'use strict';

const DISABLED_VALUES = new Set(['false', '0', 'off', 'no', 'disabled']);

function isEnabled(env = process.env) {
  const configured = env.CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED;
  if (typeof configured !== 'string') return true;
  return !DISABLED_VALUES.has(configured.trim().toLowerCase());
}

module.exports = { isEnabled };
