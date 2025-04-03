import { SubmissionResult } from './../models';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { form_styles } from '../shared';
import { FormComponentBase } from '../form.base';
import { LoginFormDataRaw, LoginFormDataOut, LoginFormObject } from './models';
import { environment } from '../../../environment/environment';
import { FormGroup, FormControl, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AsyncPipe } from '@angular/common';
import { map, Observable, of, OperatorFunction, pipe, tap } from 'rxjs';
import { AuthService } from '../../auth/auth.service';
import { JwtTokenService } from '../../auth/jwt.token.service';

@Component({
  selector: 'form.login',
  imports: [ReactiveFormsModule, FormsModule, AsyncPipe],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: `${form_styles()} rounded-tr-xl`
  }
})
export class LoginComponent extends FormComponentBase<LoginFormDataRaw, LoginFormDataOut, { token: string }> {

  formUrl = environment.loginUrl;
  authService = inject(AuthService);

  // on valid login
  override responseHandler = (response: { token: string }) => {
    const { token } = response;
    this.authService.loginFromToken(token);
  };

  constructor() {
    const formObject = new LoginFormObject();

    const formGroup = new FormGroup({
      user: new FormControl("", [Validators.required]),
      password: new FormControl("", Validators.required)
    });

    super(formObject, formGroup);

  }
}
