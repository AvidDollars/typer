import { ValidatorFn, AbstractControl, FormGroup } from "@angular/forms";
import { fromEvent, throttleTime } from 'rxjs';
import { ElementRef, inject, signal, computed } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, finalize, map, Observable, of, timer } from 'rxjs';
import { SubmissionResult, FormObject } from './models';

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

/**
 * Base class for /login /register /reset components
 */
export abstract class FormComponentBase<Raw, Out> {

  successMessage = "submitted!"; // on valid submit
  abstract formUrl: string;
  abstract formObject: FormObject<Raw, Out>;
  abstract formGroup: FormGroup;

  http = inject(HttpClient);
  formElement: HTMLFormElement = inject(ElementRef).nativeElement;
  passwordVisible = signal(false); // toggled by "show" checkbox input
  submittedInvalidForm = signal(false);
  submitBtnText = computed(() => this.submittedInvalidForm() === true ? "form is invalid!" : "submit");
  requestActive = signal(false); // if POST /register is active
  serverResponse = "server error"; // re-used in "trySendRequest" method in "server_responded_with_error" clause

  togglePasswordVisibility() {
    this.passwordVisible.update(val => !val);
  }

  showErrMsgOnInvalidSubmit() {
    this.submittedInvalidForm.set(true);
    timer(500).subscribe(() => this.submittedInvalidForm.set(false));
  }

  /**
   * Sends form data to the API. Returns "SubmissionResult" as an observable object.
   */
  trySendRequest = (): Observable<SubmissionResult> => {
    const server_responded_with_error = this.formObject.dataIsValid && this.formObject.dataUnchanged;

    if (!this.formObject.dataIsValid) {
      this.showErrMsgOnInvalidSubmit();
      return of({ state: "invalidForm", message: "some of the form fields are invalid!" });
    }

    else if (server_responded_with_error) {
      return of({ state: "submitFailed", message: this.serverResponse });
    }

    // data is valid and changed -> sent request
    else {
      this.requestActive.set(true);

      return this.http.post<SubmissionResult>(this.formUrl, this.formObject.outData)
        .pipe(
          map(_value => {
            this.formGroup.reset();
            return { state: "submitOk", message: this.successMessage } as SubmissionResult;
          }),
          catchError((err: HttpErrorResponse) => {
            const message = retrieveErrorMessage(err);
            this.serverResponse = message;
            return of<SubmissionResult>({ state: "submitFailed", message });
          }),
          finalize(() => {
            this.requestActive.set(false);
          })
        )
    }
  }
}