import { Injectable } from '@angular/core';
import { inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { ColorScheme } from './schemes';

@Injectable({
  providedIn: 'root'
})
export class ColorSchemeService {

  htmlElement = inject(DOCUMENT).documentElement;
  keyValue = "color-scheme";

  saveSchemeLocally(colorScheme: keyof typeof ColorScheme) {
    localStorage.setItem(this.keyValue, colorScheme);
  }

  /**
   * Retrieves 'color-scheme' from localStorage. If the value is null or not in the allowed list, the 'dark' scheme is set.
   */
  setColorScheme() {
    const colorScheme = localStorage.getItem("color-scheme");
    const schemeValue = (colorScheme === null || !(colorScheme in ColorScheme)) ? "dark" : colorScheme;
    this.htmlElement.setAttribute("data-theme", schemeValue);
  }
}
