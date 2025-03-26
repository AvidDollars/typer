import { ChangeDetectionStrategy, Component, ElementRef, inject, signal } from '@angular/core';
import { objectsAreSame, form_styles, mustBeEqual, retrieveErrorMessage, throttledFormSubmit$ } from '../shared';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { catchError, concatMap, finalize, map, Observable, of, scan, timer } from 'rxjs';
import { environment } from '../../../environment/environment';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { IRegFormDataOut, IRegFormDataRaw, SubmissionResult, RegFormObject, regFormBase } from '../models';
import { AsyncPipe } from '@angular/common';

@Component({
  selector: 'form.registration',
  imports: [ReactiveFormsModule, FormsModule, AsyncPipe],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: form_styles()
  }
})
export class RegisterComponent {

  http = inject(HttpClient);
  formElement: HTMLFormElement = inject(ElementRef<HTMLFormElement>).nativeElement;

  passwordVisible = signal(false); // toggled by "show" checkbox input
  submittedInvalidForm = signal(false);
  submitBtnText = signal("submit");
  requestActive = signal(false); // if POST /register is active
  registrationServerResponse = "server error"; // re-used in "trySendRequest" method in "server_responded_with_error" clause

  registration = new FormGroup({
    name: new FormControl("", [Validators.required]),
    email: new FormControl("", [Validators.required, Validators.email]),
    password: new FormGroup({
      value: new FormControl("", [Validators.required]),
      confirm: new FormControl("", [Validators.required]),
    }, {
      validators: [mustBeEqual("value", "confirm")]
    })
  });

  /**
   * Sends form data to the API. Returns "SubmissionResult" as an observable object.
   */
  trySendRequest = (formObject: RegFormObject): Observable<SubmissionResult> => {
    const server_responded_with_error = formObject.dataIsValid && formObject.dataUnchanged;

    if (!formObject.dataIsValid) {
      this.showErrMsgOnInvalidSubmit();
      return of({ state: "invalidForm", message: "some of the form fields are invalid!" });
    }

    else if (server_responded_with_error) {
      return of({ state: "submitFailed", message: this.registrationServerResponse });
    }

    // POST /register
    else {
      const { name, email, password: { value: password } } = formObject.rawData;
      const data: IRegFormDataOut = { name, email, password };
      this.requestActive.set(true);

      return this.http.post<SubmissionResult>(environment.registrationUrl, data)
        .pipe(
          map(_value => {
            this.registration.reset();
            return { state: "submitOk", message: "Submitted! Check your email :)" } as SubmissionResult;
          }),
          catchError((err: HttpErrorResponse) => {
            const message = retrieveErrorMessage(err);
            this.registrationServerResponse = message;
            return of<SubmissionResult>({ state: "submitFailed", message });
          }),
          finalize(() => this.requestActive.set(false)),
        )
    }
  }

  /**
   * Creates "ReqFormObject" from the form which is then used to send data to POST /register.
   */
  submitAction$ = throttledFormSubmit$(this.formElement, this.registration).pipe(
    // To see if current form data is changed. If data is valid but unchanged => don't send HTTP request.
    scan((accumulated: RegFormObject, current: FormGroup) => {
      const rawData = current.getRawValue() as IRegFormDataRaw;
      const dataUnchanged = objectsAreSame(rawData, accumulated.rawData);
      return { rawData, dataIsValid: current.valid, dataUnchanged };
    }, regFormBase),
    concatMap(this.trySendRequest),
  );

  togglePasswordVisibility() {
    this.passwordVisible.update(val => !val);
  }

  showErrMsgOnInvalidSubmit(message = "Form is invalid!") {
    this.submittedInvalidForm.set(true);
    this.submitBtnText.set(message);

    timer(500)
      .subscribe(_ => {
        this.submittedInvalidForm.set(false);
        this.submitBtnText.set("submit");
      });
  }
}
