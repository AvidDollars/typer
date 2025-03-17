import { ChangeDetectionStrategy, Component } from '@angular/core';
import { form_styles } from '../shared';

@Component({
  selector: 'app-register',
  imports: [],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: form_styles()
  }
})
export class RegisterComponent {

}
