import { computed, inject, Injectable, signal } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { JwtTokenService } from './jwt.token.service';
import { Router } from '@angular/router';
import { catchError, Observable, map, of } from 'rxjs';
import { LoginOperation, TokenPayload, UserCredentials } from './models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  loginUrl = environment.route("login");

  #http = inject(HttpClient);
  #jwtService = inject(JwtTokenService);
  #router = inject(Router);

  isAuthenticated = signal(this.#jwtService.tokenIsValid);
  user = computed<TokenPayload | null>(() => {
    const rawToken = this.#jwtService.getToken();
    if (this.isAuthenticated() && rawToken !== null) {
      return this.#jwtService.extractPayload(rawToken);
    } else {
      return null
    }
  });
  autoLogoutTimer?: NodeJS.Timeout;

  constructor() {
    this.initAutoLogout();
  }

  /**
   * Initializes timer for auto-logout if the token is valid and not expired.
   */
  initAutoLogout() {
    if (this.#jwtService.tokenIsValid) {
      const expiration = this.#jwtService.expirationInSeconds;
      this.autoLogoutTimer = setTimeout(() => this.logout(), expiration)
    }
  }

  /**
   * Attempts to login user. Returns an observable of "LoginOperation" as a result.
   */
  login(credentials: UserCredentials): Observable<LoginOperation> {
    return this.#http
      .post<{ token: string }>(this.loginUrl, credentials)
      .pipe(
        map(response => {
          const { token } = response;
          this.#jwtService.saveToken(token);
          this.isAuthenticated.set(this.#jwtService.tokenIsValid);
          this.initAutoLogout();
          return { status: "logged" } as LoginOperation;
        }),
        catchError((error: HttpErrorResponse) => {
          return of<LoginOperation>({ status: "errored", errorMessage: error.message, statusCode: error.status })
        }),
    ); 
  }

  logout() {
    this.isAuthenticated.set(false);
    this.#jwtService.deleteToken();
    clearTimeout(this.autoLogoutTimer);
    this.autoLogoutTimer = undefined;
    this.#router.navigateByUrl("/");
  }
}
