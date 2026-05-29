# iOS Form Components (SwiftUI)

Native SwiftUI form controls for the iOS half of `form-ux-design`. Mirror the
field anatomy, validation, and submission rules from the parent `SKILL.md` and
`references/form-validation.md`; this file covers the SwiftUI-specific control
recipes. Prefer `Form`/`List`-backed grouped layouts on iOS because they give
native section styling, swipe affordances, and Dynamic Type for free.

Minimum touch target on iOS is 44 pt. Labels go above inputs in custom layouts;
inside a `Form`, use the platform-native leading label only for short, scannable
settings rows, never as a substitute for a real field label on data-entry forms.

## 1. Text Input Fields

`TextField` is the workhorse. Bind it to view-model state and validate on commit
(`onSubmit`) or focus loss, not on every keystroke.

```swift
struct FormTextField: View {
    let label: String
    @Binding var text: String
    var placeholder: String = ""
    var supportingText: String? = nil
    var isError: Bool = false
    var keyboard: UIKeyboardType = .default
    var contentType: UITextContentType? = nil
    var submitLabel: SubmitLabel = .next

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(label)
                .font(.subheadline.weight(.medium))
                .foregroundStyle(.secondary)
            TextField(placeholder, text: $text)
                .keyboardType(keyboard)
                .textContentType(contentType)
                .submitLabel(submitLabel)
                .textFieldStyle(.roundedBorder)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .strokeBorder(isError ? Color.red : Color.clear, lineWidth: 1)
                )
            if let supportingText {
                Text(supportingText)
                    .font(.caption)
                    .foregroundStyle(isError ? .red : .secondary)
            }
        }
    }
}
```

Set `textContentType` (`.emailAddress`, `.telephoneNumber`, `.oneTimeCode`,
`.name`) so iOS offers QuickType autofill. Set `autocorrectionDisabled()` and
`textInputAutocapitalization(.never)` on email, username, and code fields.

**Password with visibility toggle:**

```swift
struct PasswordField: View {
    let label: String
    @Binding var text: String
    var isError: Bool = false
    @State private var isVisible = false

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(label).font(.subheadline.weight(.medium)).foregroundStyle(.secondary)
            HStack {
                Group {
                    if isVisible { TextField("", text: $text) }
                    else { SecureField("", text: $text) }
                }
                .textContentType(.password)
                .autocorrectionDisabled()
                .textInputAutocapitalization(.never)
                Button {
                    isVisible.toggle()
                } label: {
                    Image(systemName: isVisible ? "eye.slash" : "eye")
                }
                .accessibilityLabel(isVisible ? "Hide password" : "Show password")
            }
            .padding(10)
            .background(RoundedRectangle(cornerRadius: 8).fill(.quaternary))
        }
    }
}
```

**Multi-line with character counter:** use `TextField(_, text:, axis: .vertical)`
with `.lineLimit(3...6)`, or `TextEditor` for free-form notes. Clamp input in the
binding setter and show "N chars left" as trailing-aligned caption text that
turns red under a threshold.

## 2. Picker / Dropdown

`Picker` adapts its appearance to context. Inside a `Form` it renders as a
navigation row; the `.menu` style is the closest equivalent to a dropdown.

```swift
struct DropdownField<T: Hashable & Identifiable>: View {
    let label: String
    let options: [T]
    @Binding var selection: T?
    let display: (T) -> String

    var body: some View {
        Picker(label, selection: $selection) {
            Text("Select...").tag(T?.none)
            ForEach(options) { option in
                Text(display(option)).tag(T?.some(option))
            }
        }
        .pickerStyle(.menu)
    }
}
```

Use `.navigationLink` style inside a `Form` when the option list is long enough
to deserve its own pushed screen. Use `.segmented` only for 2-4 mutually
exclusive options that fit on one line.

| Criteria | Picker (.menu) | Segmented | Radio-style List |
|---|---|---|---|
| Options | 5+ items | 2-4 short items | 2-6 items, descriptions needed |
| Space | Compact (collapsed) | One line | One row each |
| Best for | Country, category | Yes/No, view mode | Plan choice with subtitles |

Wrong choice failure mode: a segmented control with 6+ options shrinks each label
to an unreadable, untappable sliver; a `.menu` picker for a binary yes/no hides
the choice behind an extra tap.

## 3. Toggle and Selection Controls

```swift
Toggle("Enable notifications", isOn: $notificationsOn)
    .toggleStyle(.switch)

Toggle(isOn: $marketingOptIn) {
    VStack(alignment: .leading) {
        Text("Marketing emails")
        Text("Product news and offers").font(.caption).foregroundStyle(.secondary)
    }
}
```

`Toggle` is the canonical on/off control; do not build a custom switch. For
multi-select, use a `List` with `.environment(\.editMode, .constant(.active))`
and `selection:`, or a set of `Toggle` rows. For single-select among a few
labelled options with descriptions, use a `List` of rows each showing a
checkmark on the selected one rather than forcing a `Picker`.

## 4. Date and Time Pickers

```swift
struct DateField: View {
    let label: String
    @Binding var date: Date
    var range: ClosedRange<Date>? = nil

    var body: some View {
        if let range {
            DatePicker(label, selection: $date, in: range, displayedComponents: .date)
        } else {
            DatePicker(label, selection: $date, displayedComponents: .date)
        }
    }
}
```

Use `displayedComponents: [.date, .hourAndMinute]` for combined date-time.
Inside a `Form`, `DatePicker` renders as a compact tappable field that expands a
graphical picker; this is the preferred native pattern. For open-ended ranges,
bind two `DatePicker`s and validate start <= end in the view model. iOS has no
built-in range picker, so model start and end as separate `Date` values.

## 5. Stepper and Slider

```swift
Stepper(value: $quantity, in: 1...99) {
    HStack {
        Text("Quantity")
        Spacer()
        Text("\(quantity)").monospacedDigit().foregroundStyle(.secondary)
    }
}

VStack(alignment: .leading) {
    HStack {
        Text("Budget")
        Spacer()
        Text(amount, format: .currency(code: "UGX")).foregroundStyle(.tint)
    }
    Slider(value: $amount, in: 0...1_000_000, step: 1_000)
}
```

Use `Stepper` for small, discrete counts where exact values matter (quantity,
guests). Use `Slider` for approximate magnitudes within a range. Wrong choice
failure mode: a `Slider` for a value the user must hit exactly (e.g. invoice
quantity) makes precise entry impossible; pair or replace it with a `Stepper` or
numeric `TextField`.

## 6. File and Image Pickers

```swift
import PhotosUI

struct ImagePickerField: View {
    @Binding var item: PhotosPickerItem?
    @Binding var image: Image?

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            image?
                .resizable()
                .scaledToFill()
                .frame(height: 200)
                .clipShape(RoundedRectangle(cornerRadius: 12))
            PhotosPicker(selection: $item, matching: .images) {
                Label(image == nil ? "Select Image" : "Change Image",
                      systemImage: "photo")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
        }
        .onChange(of: item) { _, newValue in
            Task {
                if let data = try? await newValue?.loadTransferable(type: Data.self),
                   let ui = UIImage(data: data) {
                    image = Image(uiImage: ui)
                }
            }
        }
    }
}
```

Use `PhotosPicker` for photos and `.fileImporter(isPresented:allowedContentTypes:)`
for documents (PDF, etc.). Show upload progress with a `ProgressView(value:)`
plus filename and percentage. Compress large images before upload per the
`image-compression` skill.

## 7. Form Layout Patterns

```swift
Form {
    Section("Contact") {
        FormTextField(label: "Name", text: $name, contentType: .name)
        FormTextField(label: "Email", text: $email,
                      keyboard: .emailAddress, contentType: .emailAddress)
    }
    Section("Details") {
        DropdownField(label: "Category", options: categories,
                      selection: $category) { $0.name }
        Toggle("Subscribe to updates", isOn: $subscribe)
    }
}
```

`Form` gives native grouped sections, correct insets, and Dynamic Type. For
paired fields (first/last name), place two `TextField`s in an `HStack` inside a
single row. Use `LabeledContent` for read-only summary rows. Present focused
sub-tasks in a `.sheet`; reserve `.fullScreenCover` for true takeovers such as
multi-step onboarding.

## 8. Multi-Step Form / Wizard

```swift
struct FormWizard: View {
    @State private var step = 0
    let steps: [AnyView]
    let labels: [String]
    let isStepValid: (Int) -> Bool
    let onSubmit: () -> Void

    var body: some View {
        VStack {
            ProgressView(value: Double(step + 1), total: Double(steps.count)) {
                Text(labels[step]).font(.headline)
            }
            .padding()

            steps[step]
            Spacer()

            HStack {
                Button("Back") { step -= 1 }
                    .disabled(step == 0)
                Spacer()
                if step < steps.count - 1 {
                    Button("Next") { step += 1 }
                        .disabled(!isStepValid(step))
                        .buttonStyle(.borderedProminent)
                } else {
                    Button("Submit", action: onSubmit)
                        .disabled(!isStepValid(step))
                        .buttonStyle(.borderedProminent)
                }
            }
            .padding()
        }
    }
}
```

The final step should be a review screen built from `LabeledContent` rows grouped
by section, each section offering an "Edit" affordance that jumps back to that
step. Persist in-progress answers so a backgrounded app does not lose entry.

## 9. Form State Management

```swift
@Observable
final class FormModel {
    var name = ""
    var email = ""
    var category: Category?
    var isSubmitting = false
    var fieldErrors: [String: String] = [:]

    var isValid: Bool {
        fieldErrors.isEmpty && !name.isEmpty && !email.isEmpty
    }

    func validate() -> Bool {
        var errs: [String: String] = [:]
        if name.isEmpty { errs["name"] = "Name is required" }
        if email.isEmpty {
            errs["email"] = "Email is required"
        } else if !email.contains("@") {
            errs["email"] = "Enter a valid email"
        }
        fieldErrors = errs
        return errs.isEmpty
    }
}
```

Drive focus with `@FocusState` and an enum of field cases; advance on
`onSubmit`. Clear a field's error the moment the user edits it again so stale
red borders do not linger.

## 10. Form Submission

```swift
extension FormModel {
    @MainActor
    func submit(using repo: Repository) async -> SubmitResult {
        guard validate() else { return .invalid }
        isSubmitting = true
        defer { isSubmitting = false }
        do {
            try await repo.submitForm(self)
            return .success
        } catch let error as ValidationError {
            fieldErrors = error.fieldErrors
            return .serverValidation
        } catch is URLError {
            return .network
        } catch {
            return .failure(error.localizedDescription)
        }
    }
}

enum SubmitResult {
    case success, invalid, serverValidation, network, failure(String)
}
```

**Submit button with loading state:**

```swift
Button {
    Task { result = await model.submit(using: repo) }
} label: {
    HStack {
        if model.isSubmitting { ProgressView().tint(.white) }
        Text(model.isSubmitting ? "Submitting..." : "Submit")
    }
    .frame(maxWidth: .infinity, minHeight: 44)
}
.buttonStyle(.borderedProminent)
.disabled(model.isSubmitting || !model.isValid)
```

On `.success` dismiss or navigate and show a confirmation; on `.network` show a
retryable alert; on `.serverValidation` scroll to and focus the first errored
field. Disable the submit button while `isSubmitting` to prevent double posts.

## Read next

- `references/form-validation.md` for cross-platform validation and error rules.
- `references/form-accessibility.md` for VoiceOver, Dynamic Type, and touch
  targets.
- The `ios-ui-ux-design` skill for broader SwiftUI navigation and screen polish.
