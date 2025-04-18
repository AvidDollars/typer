import { ActivationResult } from './../models';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { environment } from '../../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { retrieveErrorMessage } from '../shared';
import { AsyncPipe } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { catchError, concatMap, map, of } from 'rxjs';
import JSConfetti from 'js-confetti'
import { ConfettiService } from '../../confetti/confetti.service';

@Component({
  selector: 'app-activate',
  imports: [AsyncPipe],
  templateUrl: './activate.component.html',
  styleUrl: './activate.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: `
      py-8 bg-secondary rounded-xl
      place-items-center grid
      row-start-1 col-span-full row-span-full
      md:col-start-2 md:col-span-4
      lg:col-start-3 lg:col-span-2

      [&>p]:rounded-md [&>p]:p-4 [&>p]:text-xl
    `
  }
})
export class ActivateComponent {

  http = inject(HttpClient);
  activatedRoute = inject(ActivatedRoute);
  confettiService = inject(ConfettiService);

  serverResponse$ = this.activatedRoute.paramMap.pipe(
    map(paramMap => paramMap.get("token")!), // presence of token is guaranteed
    map(token => environment.activateUrl(token)),
    concatMap(
      url => this.http.get<{ message: string }>(url).pipe(
        map(messageObj => {
          this.confettiService.celebrate(); // confetti explosion if successful account activation
          return { detail: messageObj.message, activated: true } as ActivationResult;
        }),
        catchError(
          (err) => {
            const detail = retrieveErrorMessage(err);
            return of<ActivationResult>({ detail, activated: false });
          }
        )
      )
    )
  )
}
