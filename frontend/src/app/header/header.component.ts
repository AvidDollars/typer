import { ChangeDetectionStrategy, Component } from '@angular/core';
import { TitleComponent } from './title/title.component';
import { UserSpaceComponent } from './user-space/user-space.component';

@Component({
  selector: 'app-header',
  imports: [
    TitleComponent, UserSpaceComponent,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderComponent {
}
