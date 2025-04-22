import { inject, Injectable } from '@angular/core';
import { SaveSessionResult, Session } from './models';
import { Observable, of, map, catchError } from 'rxjs';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { environment } from '../../environment/environment';
import { retrieveErrorMessage } from '../user/shared';

/**
 * Service used to work with "/typing-sessions" endpoints.
 */
@Injectable({
  providedIn: 'root'
})
export class SessionService {

  http = inject(HttpClient);

  saveSession$(session: Session): Observable<SaveSessionResult> {
    return this.http.post<null>(environment.saveSessionUrl, session).pipe(
      map(() => ({ state: "saved" } as SaveSessionResult)),
      catchError((err: HttpErrorResponse) => {
        const message = retrieveErrorMessage(err);
        return of({ state: "failed", message } as SaveSessionResult);
      })
    )
  }
}
