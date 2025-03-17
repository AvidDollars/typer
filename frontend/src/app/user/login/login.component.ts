import { ChangeDetectionStrategy, Component } from '@angular/core';
import { form_styles } from '../shared';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: form_styles()
  }
})
export class LoginComponent {

}
