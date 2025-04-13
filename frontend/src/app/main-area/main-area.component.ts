import { ChangeDetectionStrategy, Component, effect, ElementRef, inject, OnDestroy, OnInit, signal, viewChild } from '@angular/core';
import { filter, fromEvent, map, scan, takeWhile, finalize, timer } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { TextLoaderService } from './text-loader.service';
import { discardIrrelevantKeys, extractKey } from './utils';
import JSConfetti from 'js-confetti';
import { toObservable } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-main-area',
  imports: [AsyncPipe],
  templateUrl: './main-area.component.html',
  styleUrl: './main-area.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: `
      overflow-scroll no-scrollbar
      relative bg-light rounded-xl p-2
      col-start-3 col-span-2 row-span-5
      border-5 border-double border-secondary
    `,
    "[style.fontFamily]": "'Roboto Mono'",
  }
})
export class MainAreaComponent implements OnInit, OnDestroy {

  hostElement = inject(ElementRef).nativeElement as HTMLElement;
  textareaElement = viewChild<ElementRef<HTMLTextAreaElement>>("textarea");
  textareaFocus$ = toObservable(this.textareaElement).pipe( // to retrieve lost focus on textarea
    filter(value => value != undefined),
    map(textarea => textarea.nativeElement.focus()),
  );

  // TODO: create confetti service
  confetti = new JSConfetti(); // confetti at the end of typing session

  textLoaderService = inject(TextLoaderService);
  loadedText = this.textLoaderService.text;
  characterArray: string[] = [];
  finishedTyping = signal(false);

  // TYPING STREAM
  typing$ = fromEvent<KeyboardEvent>(this.hostElement, "keydown").pipe(
    filter(discardIrrelevantKeys), // to filter out "Shift" / "CapsLock" / etc...
    map(extractKey),
    scan((acc, key) => {
      let index = (key === "Backspace") ? --acc[0] : ++acc[0];
      index = (index < 0) ? -1 : index; // min index: -1
      return [index, key] as [number, string];
    }, [-1, ""] as [number, string]),
    takeWhile(([index, _key]) => index < this.characterArray.length - 1), // TODO: you must add extra char to finish the session
    map(([index, char]) => {
      return [index, char, this.characterArray[index] === char] as [number, string, boolean];
    }),
    scan((error_counter, [_index, key, isCorrectKey]) => {
      if (!isCorrectKey && key !== "Backspace") {
        error_counter.set(key, (error_counter.get(key) ?? 0) + 1)
      };
      return error_counter;
    }, new Map(this.characterArray.map(char => [char, 0]))),
    finalize(() => {
      timer(200).subscribe(() => {
        this.finishedTyping.set(true);
        this.confetti.addConfetti();
      });
      timer(5000).subscribe(() => {
        this.confetti.destroyCanvas();
      })
    }),
  );

  constructor() {
    // TODO: computed / linkedSignal instead?
    effect(() => { // new text -> new character array
      let text = this.loadedText() ?? "";
      this.characterArray = [...text];
    });
  }

  ngOnInit() {
    this.hostElement.scrollTo({ top: 0, behavior: "smooth" });
    this.typing$.subscribe(v => console.log("v: ", v));

    // TODO: autoscrolling
    //interval(50).pipe(delay(2_000)).subscribe(val => this.host.scrollTo({top: val / 5, behavior: "smooth"}))
  }

  ngOnDestroy() {
    this.confetti.destroyCanvas();
  }
}
