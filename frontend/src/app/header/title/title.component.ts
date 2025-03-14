import { AsyncPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { interval, map, scan, takeWhile } from 'rxjs';

@Component({
  selector: 'app-title',
  imports: [AsyncPipe],
  templateUrl: './title.component.html',
  styleUrl: './title.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: "md:w-48 lg:w-64"
  }
})
export class TitleComponent {

  #subtitle = "practise typing like a pro!";
  #mistakeIndex = 3;
  #extraIndex = 4; // to compensate "deletion" operation

  // runs "typing with error" sequence
  subtitle$ = interval(80).pipe(
    takeWhile(index => index < this.#subtitle.length + this.#extraIndex),
    map(index =>
      (index > this.#mistakeIndex + this.#mistakeIndex)
        ? this.#subtitle.at(index - this.#extraIndex)!
        : this.#subtitle.at(index)!
    ),
    scan((text: string[], char, index) => {
      if (index === this.#mistakeIndex) {
        return [...text, "o"];
      } else if (index === this.#mistakeIndex + 2 || index === this.#mistakeIndex + 3) {
        text.pop();
        return text;
      } else {
        return [...text, char];
      }
    }, []),
    map(text => text.join("")),
  )
}
