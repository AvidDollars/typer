import { ChangeDetectionStrategy, Component } from '@angular/core';
import { TitleComponent } from './title/title.component';
import { UserSpaceComponent } from './user-space/user-space.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-header',
  imports: [
    TitleComponent, UserSpaceComponent, RouterLink
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderComponent {
}
