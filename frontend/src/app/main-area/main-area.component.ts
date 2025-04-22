import { ChangeDetectionStrategy, Component, effect, ElementRef, inject, OnInit, viewChild } from '@angular/core';
import { filter, map, scan, takeWhile, finalize, interval, Subject, fromEvent, takeUntil, startWith, concatMap, tap } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { TextLoaderService } from './text-loader.service';
import { discardIrrelevantKeys, extractKey, SessionState } from './utils';
import { toObservable } from '@angular/core/rxjs-interop';
import { ConfettiService } from '../confetti/confetti.service';
import { ClockPipe } from '../clock/clock.pipe';
import { SessionService } from '../session/session.service';
import { Session } from '../session/models';

@Component({
  selector: 'app-main-area',
  imports: [AsyncPipe, ClockPipe],
  templateUrl: './main-area.component.html',
  styleUrl: './main-area.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,

  // TODO: improve layout for small screens
  host: {
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
  loadedTextId = this.textLoaderService.textId;

  sessionState = new SessionState();
  sessionService = inject(SessionService);
  activeTypoos = this.sessionState.activeTypoos;
  hostElement = inject(ElementRef).nativeElement as HTMLElement;
  textareaElement = viewChild<ElementRef<HTMLTextAreaElement>>("textarea");

  constructor() {
    // TODO: try to create better solution which does not involve using "effect"
    effect(() => { // new text -> new character array
      const text = this.loadedText() ?? "";
      const textId = this.loadedTextId() ?? "";
      this.sessionState.loadText(text, textId);
    });
  }

  ngOnInit() {
    this.hostElement.scrollTo({ top: 0, behavior: "smooth" });

    // TODO: autoscrolling
    //interval(50).pipe(delay(2_000)).subscribe(val => this.host.scrollTo({top: val / 5, behavior: "smooth"}))
  }

  initTextarea$ = toObservable(this.textareaElement).pipe(
    filter(Boolean),
    map(textarea => {
      const element = textarea.nativeElement;
      element.focus(); // to retrieve lost focus on textarea when going to a different page
      element.addEventListener("input", this.initTypingSession); // triggers "typing$" and "clock$"
      element.textContent = ""; // TODO: there is for some reason 2 empty spaces present
    }),
  );

  // TYPING SESSION TRIGGERS
  startTyping$ = new Subject<void>();
  sessionFinished$ = new Subject<Session>();
  onSessionFinished$ = this.sessionFinished$.pipe(
    filter(Boolean),
    concatMap(session => this.sessionService.saveSession$(session)),
    tap(() => this.confettiService.celebrate()),
  );

  /**
   * Initializes typing session and immediately removes itself as event listener.
   */
  initTypingSession = () => {
    this.startTyping$.next();
    this.sessionState.markStart();
    this.textareaElement()?.nativeElement.removeEventListener("input", this.initTypingSession);
  }

  // TYPING
  typing$ = this.startTyping$.pipe(
    startWith(null), // to start the stream on 1st keystroke
    concatMap(() => fromEvent<KeyboardEvent>(this.hostElement, "keydown")),
    filter(discardIrrelevantKeys), // to filter out "Shift" / "CapsLock" / etc...
    map(extractKey),
    scan((state, char) => state.updateState(char), this.sessionState),
    takeWhile(state => !state.isFinished),
    finalize(() => this.sessionFinished$.next(this.sessionState.results)),
  );

  // CLOCK
  clock$ = this.startTyping$.pipe(
    concatMap(() => interval(1000).pipe(
      // Time between calls in operators is bigger than value specified in "interval" observable.
      // TODO: implement clock which will correct itself, so that "duration of session = elapsed time on clock"
      map(value => value + 1),
      startWith(0),
      takeUntil(this.sessionFinished$),
    )),
  );
}
