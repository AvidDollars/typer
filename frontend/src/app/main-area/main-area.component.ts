import { ChangeDetectionStrategy, Component, effect, ElementRef, inject, OnInit, signal, viewChild } from '@angular/core';
import { filter, map, scan, takeWhile, finalize, timer, interval, Subject, fromEvent, takeUntil, startWith, concatMap } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { TextLoaderService } from './text-loader.service';
import { discardIrrelevantKeys, extractKey } from './utils';
import { toObservable } from '@angular/core/rxjs-interop';
import { ConfettiService } from '../confetti/confetti.service';

@Component({
  selector: 'app-main-area',
  imports: [AsyncPipe],
  templateUrl: './main-area.component.html',
  styleUrl: './main-area.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { // TODO: improve layout for small screens
    class: `
      overflow-scroll no-scrollbar
      relative bg-light rounded-xl p-2
      border-5 border-double border-secondary

      col-span-full row-span-3 row-start-1
      md:col-start-2 md:col-span-4 md:row-span-5
      lg:col-start-3 lg:col-span-2 lg:row-span-5
    `,
    "[style.fontFamily]": "'Roboto Mono'",
  }
})
export class MainAreaComponent implements OnInit {

  confettiService = inject(ConfettiService); // confetti at the end of typing session
  textLoaderService = inject(TextLoaderService);
  loadedText = this.textLoaderService.text;
  characterArray: string[] = [];
  finishedTyping = signal(false);

  hostElement = inject(ElementRef).nativeElement as HTMLElement;
  textareaElement = viewChild<ElementRef<HTMLTextAreaElement>>("textarea");

  initTextarea$ = toObservable(this.textareaElement).pipe(
    filter(value => value != undefined),
    map(textarea => {
      const element = textarea.nativeElement;
      element.focus(); // to retrieve lost focus on textarea when going to a different page
      element.addEventListener("input", this.initTypingSession); // triggers "typing$" and "clock$"
    }),
  );

  // TYPING SESSION TRIGGERS
  startTyping$ = new Subject<void>();
  endTyping$ = new Subject<void>();

  typingStream$ = fromEvent<KeyboardEvent>(this.hostElement, "keydown").pipe(
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
      this.endTyping$.next();
      this.finishedTyping.set(true);

      timer(200).subscribe(() => {
        this.confettiService.celebrate();
      });
    }),
  );

  // TYPING
  typing$ = this.startTyping$.pipe(
    concatMap(() => this.typingStream$),
  );

  // CLOCK
  clock$ = this.startTyping$.pipe(
    concatMap(() => interval(10).pipe(
      map(value => value + 1),
      startWith(0),
      takeUntil(this.endTyping$)
    )),
  );

  constructor() {
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

  /**
   * Initializes typing session and immediately removes itself as event listener.
   */
  initTypingSession = () => {
    this.startTyping$.next();
    this.textareaElement()?.nativeElement.removeEventListener("input", this.initTypingSession)
  }
}
