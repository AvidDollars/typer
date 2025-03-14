import { Injectable, inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { ColorScheme } from './schemes';

@Injectable({
  providedIn: 'root'
})
export class ColorSchemeService {

  #htmlElement = inject(DOCUMENT).documentElement;
  #keyValue = "color-scheme";

  saveSchemeLocally(colorScheme: keyof typeof ColorScheme): void {
    localStorage.setItem(this.#keyValue, colorScheme);
  }

  /**
   * If an argument is provided, it will be used as value for color scheme.
   * If an argument is missing, it retrieves 'color-scheme' from localStorage.
   * If the value from localStorage is null or not in the allowed list, the 'dark' scheme is set.
   */
  setColorScheme(value: null | keyof typeof ColorScheme = null): void {
    if (value !== null) {
      this.#htmlElement.setAttribute("data-theme", value);
      return;
    }
    const colorScheme = localStorage.getItem(this.#keyValue);
    const schemeValue = (colorScheme === null || !(colorScheme in ColorScheme)) ? "dark" : colorScheme;
    this.#htmlElement.setAttribute("data-theme", schemeValue);
  }
}
