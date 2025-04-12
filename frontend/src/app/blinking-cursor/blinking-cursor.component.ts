import { AsyncPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, inject, input } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';
import { tap, filter, concatMap, timer } from 'rxjs';

/**
 * used in "typing" intro
 */
@Component({
  selector: 'app-blinking-cursor',
  imports: [AsyncPipe],
  template: `
    {{ destroyCursor$ | async }} <!-- destroys blinking cursor if "durationMs" input is provided -->
    <ng-container>|</ng-container>
  `,
  styles: `
    :host.blinking-cursor { // TODO: check if PROD build has "-moz-animation / -ms-animation / etc..."
      animation: 1s blink step-end infinite;
    };

    @keyframes blink { // TODO: check if PROD build has "@-moz-keyframes / @-webkit-keyframes / etc..."
      from, to {
        color: transparent;
      };
      50% {
        color: var(--color-text);
      };
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: "blinking-cursor",
    "[style.fontSize.px]": "fontSizePx()",
    "[style.fontWeight]": "fontWeight()",
  }
})
export class BlinkingCursorComponent {
  fontSizePx = input(20);
  fontWeight = input(300);
  durationMs = input<number>();
  host = inject(ElementRef).nativeElement as HTMLElement;

  // destroys the component if "durationMs" input is provided
  destroyCursor$ = toObservable(this.durationMs).pipe(
    filter(value => value != undefined),
    concatMap(value => timer(value).pipe(
      tap(() => this.host.remove()),
    ))
  );
}
