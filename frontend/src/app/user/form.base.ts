import { FormGroup } from "@angular/forms";
import { ElementRef, inject, signal, computed } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, finalize, map, Observable, of, timer, concatMap } from 'rxjs';
import { SubmissionResult, FormObject } from './models';
import { throttledFormSubmit, retrieveErrorMessage } from "./shared";

/**
 * Base class for /login, /register, and /reset components.
 * "Raw" generic param: raw data from FormGroup
 * "Out" generic param: data to be used in HTTP request
 */
export abstract class FormComponentBase<
  Raw extends object,
  Out extends object,
  Res = void, // shape of the HTTP response
> {

  http = inject(HttpClient);
  formElement: HTMLFormElement = inject(ElementRef).nativeElement;

  abstract formUrl: string;
  successMessage = "submitted!"; // on valid submit
  submitAction$: Observable<SubmissionResult>;
  passwordVisible = signal(false); // toggled by "show" checkbox input
  submittedInvalidForm = signal(false);
  submitBtnText = computed(() => this.submittedInvalidForm() === true ? "form is invalid!" : "submit");
  requestActive = signal(false); // if POST /register is active
  serverResponse = "server error"; // re-used in "trySendRequest" method in "server_responded_with_error" clause
  responseHandler?: (res: Res) => void; // handles successful HTTP responses

  constructor(
    public formObject: FormObject<Raw, Out>,
    public formGroup: FormGroup
  ) {

    this.submitAction$ = throttledFormSubmit(this.formElement, this.formGroup, this.formObject).pipe(
      concatMap(this.trySendRequest)
    );
  }

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

      return this.http.post<Res>(this.formUrl, this.formObject.outData)
        .pipe(
          map(value => {
            this.formGroup.reset();
            this.responseHandler?.(value); // response data handler (e.g. handling JWT token for /login)

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