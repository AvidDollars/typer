import { computed, inject, Injectable, OnDestroy, signal } from '@angular/core';
import { JwtTokenService } from './jwt.token.service';
import { Router } from '@angular/router';
import { TokenPayload } from './models';

@Injectable({
  providedIn: 'root'
})
export class AuthService implements OnDestroy {

  #jwtService = inject(JwtTokenService);
  #router = inject(Router);

  isAuthenticated = signal(this.#jwtService.tokenIsValid);
  user = computed<TokenPayload | null>(() => {
    const rawToken = this.#jwtService.getToken();
    return (this.isAuthenticated() && rawToken !== null)
      ? this.#jwtService.extractPayload(rawToken)
      : null;
  });
  autoLogoutTimer?: NodeJS.Timeout;

  constructor() {
    this.initAutoLogout();
  }

  ngOnDestroy() {
    clearInterval(this.autoLogoutTimer);
  }

  /**
   * Initializes timer for auto-logout if the token is valid and not expired.
   */
  initAutoLogout() {
    if (this.#jwtService.tokenIsValid) {
      const expiration = this.#jwtService.expirationInSeconds;
      this.autoLogoutTimer = setTimeout(() => this.logout(), expiration * 1000);
    } else {
      this.logout();
    }
  }

  /**
   * Performs login operation from provided JWT token.
   */
  loginFromToken(token: string) {
    this.#jwtService.saveToken(token);
    this.isAuthenticated.set(this.#jwtService.tokenIsValid);
    this.initAutoLogout();
  }

  /**
   * Logout operation.
   */
  logout(navigateTo?: string) {
    this.isAuthenticated.set(false);
    this.#jwtService.deleteToken();
    clearTimeout(this.autoLogoutTimer);
    this.autoLogoutTimer = undefined;

    if (navigateTo != undefined) {
      this.#router.navigateByUrl(navigateTo);
    }
  }
}
