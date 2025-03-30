import { ChangeDetectionStrategy, Component } from '@angular/core';
import { form_styles, mustBeEqual } from '../shared';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { environment } from '../../../environment/environment';
import { RegFormDataOut, RegFormDataRaw, RegFormObject } from './models';
import { AsyncPipe } from '@angular/common';
import { FormComponentBase } from '../form.base';

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

  constructor() {
    const formObject = new RegFormObject();

    const formGroup = new FormGroup({
      name: new FormControl("", [Validators.required]),
      email: new FormControl("", [Validators.required, Validators.email]),
      password: new FormGroup({
        value: new FormControl("", [Validators.required]),
        confirm: new FormControl("", [Validators.required]),
      }, {
        validators: [mustBeEqual("value", "confirm")]
      })
    });

    super(formObject, formGroup);
  }
}
