import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-user-space',
  imports: [RouterLink],
  templateUrl: './user-space.component.html',
  styleUrl: './user-space.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserSpaceComponent {

}
