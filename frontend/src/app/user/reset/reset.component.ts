import { ChangeDetectionStrategy, Component } from '@angular/core';
import { form_styles } from '../shared';

@Component({
  selector: 'app-reset',
  imports: [],
  templateUrl: './reset.component.html',
  styleUrl: './reset.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: form_styles()
  }
})
export class ResetComponent {

}
