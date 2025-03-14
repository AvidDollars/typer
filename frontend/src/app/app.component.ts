import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { ColorSchemeService } from './color-scheme/color-scheme.service';

@Component({
    selector: 'app-root',
    imports: [
      HeaderComponent, RouterOutlet
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {

  colorSchemeService = inject(ColorSchemeService);

  ngOnInit(): void {
    this.colorSchemeService.setColorScheme();
  }
}
