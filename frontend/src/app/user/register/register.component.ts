import { ChangeDetectionStrategy, Component, } from '@angular/core';
import { objectsAreSame, form_styles, mustBeEqual, throttledFormSubmit$, FormComponentBase } from '../shared';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { concatMap, scan } from 'rxjs';
import { environment } from '../../../environment/environment';
import { RegFormDataOut, RegFormDataRaw, RegFormObject } from './models';
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
export class RegisterComponent extends FormComponentBase<RegFormDataRaw, RegFormDataOut> {

  override successMessage = "Submitted! Check your email :)";
  formUrl = environment.registrationUrl;
  formObject = new RegFormObject();

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
   * Creates "ReqFormObject" from the form which is then used to send data to POST /register.
   */
  submitAction$ = throttledFormSubmit$(this.formElement, this.formGroup).pipe(
    // To see if current form data is changed. If data is valid but unchanged => don't send HTTP request.
    scan((accumulated: RegFormObject, current: FormGroup) => {

      const currentRawData = current.getRawValue() as RegFormDataRaw;
      const dataUnchanged = objectsAreSame(currentRawData, accumulated.rawData);

      this.formObject.dataIsValid = current.valid;
      this.formObject.dataUnchanged = dataUnchanged
      this.formObject.rawData = currentRawData;

      return this.formObject
    }, this.formObject),

    concatMap(this.trySendRequest),
  );
}
