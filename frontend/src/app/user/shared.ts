import { ValidatorFn, AbstractControl, FormGroup } from "@angular/forms";
import { HttpErrorResponse } from '@angular/common/http';
import { map, Observable, scan, fromEvent, throttleTime } from 'rxjs';
import { FormObject } from './models';

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
 * Returns throttled FormObject whose state is being tracked in "scan" rxjs operator.
 */
export function throttledFormSubmit<Raw extends object, Out extends object>(
  form: HTMLFormElement,
  formGroup: FormGroup,
  formObject: FormObject<Raw, Out>,
  throttleMs = 1000,
): Observable<FormObject<Raw, Out>> {
  return fromEvent<SubmitEvent>(form, "submit")
    .pipe(
      map(event => {
        event.preventDefault();
        return formGroup;
      }),
      throttleTime(throttleMs),

      // To see if current form data is changed and valid.
      // If data is valid but unchanged => HTTP request should not be sent.
      scan((accumulated: FormObject<Raw, Out>, current: FormGroup) => {
        const currentRawData = current.getRawValue() as Raw;
        const dataUnchanged = objectsAreSame(currentRawData, accumulated.rawData);

        formObject.dataIsValid = current.valid;
        formObject.dataUnchanged = dataUnchanged;
        formObject.rawData = currentRawData;

        return formObject;
      }, formObject),
    )
}
