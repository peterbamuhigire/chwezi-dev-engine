# Account settings: delete-account confirmation dialog

`web/confirm-dialog.html` holds the markup; `web/dialog-controller.js` holds the behaviour and
exports `createConfirmDialog(options)` (CommonJS in tests, a global in the browser).

The controller uses only these DOM features, so it can be tested without a browser: `hidden`,
`disabled`, `focus()`, `textContent`, `setAttribute` / `removeAttribute` / `getAttribute`,
`isConnected`, `contains()` and `document.activeElement`. The dialog is shown and hidden with the
`hidden` attribute.

## Options

`{ document, trigger, dialog, confirmButton, cancelButton, errorRegion, fallbackFocus, perform, makeKey }`

- `perform(idempotencyKey)` returns a promise for the server call that deletes the account.
- `makeKey()` returns a fresh idempotency key; `fallbackFocus` is a focusable element (the page
  heading) used when the trigger no longer exists.

## Returned API

`open()`, `cancel()`, `confirm()` (returns a promise), `handleKeydown(event)`, `isOpen()`.

## Product contract

1. Opening moves focus into the dialog (the safe choice, Cancel, for a destructive action).
2. Cancel, and Escape while idle, close the dialog and return focus to the trigger; if the trigger
   has been removed, focus goes to `fallbackFocus`. Focus is never left on `body`.
3. While the deletion is in flight both buttons are disabled, the dialog carries
   `aria-busy="true"`, Escape is ignored and a second confirm does nothing.
4. On failure the dialog stays open, the error text is shown in the live error region, the
   buttons are enabled again and focus is placed inside the dialog so the user can retry.
5. A retry of the same deletion reuses the same idempotency key, so the server never deletes
   twice. A new deletion (after a successful one) uses a new key.
6. On success the dialog closes and focus returns as in rule 2.

Markup: the dialog has an accessible name and description, is modal to assistive technology, the
error region is announced, and both actions are real buttons.
