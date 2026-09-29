(function (root) {
  'use strict';

  // Delete-account confirmation dialog. See README.md for the contract.
  function createConfirmDialog(options) {
    const { document, trigger, dialog, confirmButton, cancelButton, errorRegion, perform } = options;
    const fallbackFocus = options.fallbackFocus || null;
    let counter = 0;
    const makeKey = options.makeKey || (() => `delete-${Date.now().toString(36)}-${(counter += 1)}`);

    let opener = null;
    let key = null; // one key per deletion; kept across retries, cleared only after success
    let busy = false;
    let open = false;

    function setBusy(value) {
      busy = value;
      confirmButton.disabled = value;
      cancelButton.disabled = value;
      if (value) dialog.setAttribute('aria-busy', 'true');
      else dialog.removeAttribute('aria-busy');
    }

    function restoreFocus() {
      const target = opener && opener.isConnected ? opener : fallbackFocus;
      if (target && target.isConnected) target.focus();
    }

    function close(completed) {
      dialog.hidden = true;
      open = false;
      if (completed) key = null;
      restoreFocus();
    }

    return {
      open() {
        if (open) return;
        opener = trigger || (document && document.activeElement) || null;
        if (key === null) key = makeKey();
        errorRegion.textContent = '';
        dialog.hidden = false;
        open = true;
        cancelButton.focus();
      },
      cancel() {
        if (!open || busy) return;
        close(false);
      },
      handleKeydown(event) {
        if (!open || event.key !== 'Escape') return;
        if (typeof event.preventDefault === 'function') event.preventDefault();
        if (!busy) close(false);
      },
      async confirm() {
        if (!open || busy) return;
        setBusy(true);
        errorRegion.textContent = '';
        try {
          await perform(key);
        } catch (error) {
          setBusy(false);
          errorRegion.textContent = 'The account was not deleted. Check your connection and try again.';
          confirmButton.textContent = 'Try again';
          confirmButton.focus();
          return;
        }
        setBusy(false);
        close(true);
      },
      isOpen() {
        return open;
      },
    };
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = { createConfirmDialog };
  else root.createConfirmDialog = createConfirmDialog;
})(this);
