import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-user-space',
  imports: [RouterLink],
  templateUrl: './user-space.component.html',
  styleUrl: './user-space.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserSpaceComponent {
  authService = inject(AuthService);
}
