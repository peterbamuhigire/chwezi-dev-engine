(function (root) {
  'use strict';

  function createConfirmDialog(options) {
    const { trigger, dialog, confirmButton, errorRegion, perform } = options;
    const makeKey = options.makeKey || (() => String(Date.now()));

    function close() {
      dialog.hidden = true;
      trigger.focus();
    }

    return {
      open() {
        dialog.hidden = false;
        confirmButton.focus();
      },
      cancel() {
        close();
      },
      handleKeydown(event) {
        if (event.key === 'Escape') close();
      },
      async confirm() {
        confirmButton.disabled = true;
        try {
          await perform(makeKey());
          confirmButton.disabled = false;
          close();
        } catch (error) {
          confirmButton.disabled = false;
          dialog.hidden = true;
          errorRegion.textContent = 'Could not delete the account.';
        }
      },
      isOpen() {
        return !dialog.hidden;
      },
    };
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = { createConfirmDialog };
  else root.createConfirmDialog = createConfirmDialog;
})(this);
