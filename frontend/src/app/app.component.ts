import { Component, inject, OnInit } from '@angular/core';
import { NavigationStart, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { ColorSchemeService } from './color-scheme/color-scheme.service';
import { filter, map } from 'rxjs';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-root',
  imports: [
    HeaderComponent, RouterOutlet, RouterLink, RouterLinkActive
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {

  colorSchemeService = inject(ColorSchemeService);
  router = inject(Router);
  #formURL = this.router.events.pipe(
    filter(event => event instanceof NavigationStart),
    map(event => ["/login", "/register", "/reset"].some(endopoint => endopoint === event.url)),
    takeUntilDestroyed(),
  )
  visibleHeader = toSignal(this.#formURL); // form header is visible only if you are on /login | /register | /reset url

  ngOnInit(): void {
    this.colorSchemeService.setColorScheme();
  }
}
