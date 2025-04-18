import { Injectable } from '@angular/core';
import JSConfetti from 'js-confetti';

@Injectable({
  providedIn: 'root'
})
export class ConfettiService {

  #confetti = new JSConfetti();

  celebrate() {
    this.#confetti.addConfetti(); // TODO: lagging on mobile device. Add less confetti?
  }
}
