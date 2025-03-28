import { HttpErrorResponse } from '@angular/common/http';
import { ValidatorFn, AbstractControl, FormGroup } from "@angular/forms";
import { Observable, fromEvent, map, throttleTime, tap, scan } from 'rxjs';

/**
 * CSS classes for /login /register /reset forms
 */
export function form_styles(): string {
  return `
    py-8 bg-secondary

    grid grid-cols-6 grid-rows-7 row-start-2 col-span-full row-span-full
    place-self-center w-full h-full rounded-b-xl

    md:col-start-2 md:col-span-4
    lg:col-start-3 lg:col-span-2

    [&_input]:bg-secondary-light [&_input]:rounded-md [&_input]:h-1/2 [&_input]:pl-2

    [&_.control,&_.control-group]:col-start-2 [&_.control,&_.control-group]:col-span-4
    [&_.control]:flex [&_.control]:flex-col

    [&_.control-group]:row-span-2
  `
}

/**
 * Check for the equality of two values. If at least one of the fields does not exist, error will be thrown.
 */
export function mustBeEqual(fieldA: string, fieldB: string): ValidatorFn {
  return (control: AbstractControl) => {
    const a = control.get(fieldA);
    const b = control.get(fieldB);

    const errMessage = (field: string) => `Form validation error occurred! Field "${field}" does not exist on the form.`;

    if (a == null) {
      throw new Error(errMessage(fieldA));
    }

    if (b == null) {
      throw new Error(errMessage(fieldB));
    }

    return (a.value === b.value) ? null : { valuesNotEqual: true };
  };
}

/**
 * Extracts error message from the API.
 */
export function retrieveErrorMessage(error: HttpErrorResponse): string {
  const { error: err } = error
  const extractedError = err.message ?? err.detail;

  if (typeof extractedError === "string") {
    return extractedError;
  } else {
    // TODO: logging
    const message = "unsuccessful action";
    console.log(message);
    console.log(error);
    return message;
  }
}

/**
 *  TODO: create more robust and efficient object comparison.
 */
export function objectsAreSame(objA: object, objB: object): boolean {
  return JSON.stringify(objA) === JSON.stringify(objB);
}

/**
 * Attaches "submit" action on provided form element.
 * Returns throttled FormGroup provided as second argument.
 */
export function throttledFormSubmit$(
  form: HTMLFormElement,
  formGroup: FormGroup,
  throttleMs = 1000
): Observable<FormGroup> {
  return fromEvent<SubmitEvent>(form, "submit")
    .pipe(
      map(event => {
        event.preventDefault();
        return formGroup;
      }),
      throttleTime(throttleMs),
    )
}
