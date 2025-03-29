import { FormObject } from './../models';
import { ChangeDetectionStrategy, Component, } from '@angular/core';
import { objectsAreSame, form_styles, mustBeEqual, retrieveErrorMessage, throttledFormSubmit$, FormComponentBase } from '../shared';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { catchError, concatMap, finalize, map, Observable, of, scan, timer } from 'rxjs';
import { environment } from '../../../environment/environment';
import { HttpErrorResponse } from '@angular/common/http';
import { SubmissionResult } from '../models';
import { RegFormDataRaw, regFormBase } from './models';
import { AsyncPipe } from '@angular/common';

@Component({
  selector: 'form.registration',
  imports: [ReactiveFormsModule, FormsModule, AsyncPipe],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: `${form_styles()} rounded-t-xl`
  }
})
export class RegisterComponent extends FormComponentBase {

  formUrl = environment.registrationUrl;

  formGroup = new FormGroup({
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
  trySendRequest = (formObject: FormObject<RegFormDataRaw>): Observable<SubmissionResult> => {
    const server_responded_with_error = formObject.dataIsValid && formObject.dataUnchanged;

    if (!formObject.dataIsValid) {
      this.showErrMsgOnInvalidSubmit();
      return of({ state: "invalidForm", message: "some of the form fields are invalid!" });
    }

    else if (server_responded_with_error) {
      return of({ state: "submitFailed", message: this.serverResponse });
    }

    // POST /register
    else {
      const { name, email, password: { value: password } } = formObject.rawData;
      this.requestActive.set(true);

      return this.http.post<SubmissionResult>(this.formUrl, { name, email, password })
        .pipe(
          map(_value => ({ state: "submitOk", message: "Submitted! Check your email :)" }) as SubmissionResult),
          catchError((err: HttpErrorResponse) => {
            const message = retrieveErrorMessage(err);
            this.serverResponse = message;
            return of<SubmissionResult>({ state: "submitFailed", message });
          }),
          finalize(() => {
            this.formGroup.reset();
            this.requestActive.set(false);
          })
        )
    }
  }

  /**
   * Creates "ReqFormObject" from the form which is then used to send data to POST /register.
   */
  submitAction$ = throttledFormSubmit$(this.formElement, this.formGroup).pipe(
    // To see if current form data is changed. If data is valid but unchanged => don't send HTTP request.
    scan((accumulated: FormObject<RegFormDataRaw>, current: FormGroup) => {
      const rawData = current.getRawValue() as RegFormDataRaw;
      const dataUnchanged = objectsAreSame(rawData, accumulated.rawData);
      return { rawData, dataIsValid: current.valid, dataUnchanged };
    }, regFormBase),
    concatMap(this.trySendRequest),
  );
}
