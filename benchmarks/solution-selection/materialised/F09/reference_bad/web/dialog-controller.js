(function (root) {
  'use strict';

  function createConfirmDialog(options) {
    const { trigger, dialog, confirmButton, cancelButton, errorRegion, perform } = options;
    const makeKey = options.makeKey || (() => String(Date.now()));

    function close() {
      dialog.hidden = true;
      trigger.focus();
    }

    return {
      open() {
        errorRegion.textContent = '';
        dialog.hidden = false;
        cancelButton.focus();
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
        } catch (error) {
          confirmButton.disabled = false;
          errorRegion.textContent = 'Could not delete the account. Please try again.';
          confirmButton.focus();
          return;
        }
        confirmButton.disabled = false;
        close();
      },
      isOpen() {
        return !dialog.hidden;
      },
    };
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = { createConfirmDialog };
  else root.createConfirmDialog = createConfirmDialog;
})(this);
