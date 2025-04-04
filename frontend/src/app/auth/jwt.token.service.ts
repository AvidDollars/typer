import { Injectable } from '@angular/core';
import { TokenPayload } from './models';


@Injectable({
  providedIn: 'root'
})
export class JwtTokenService {

  #key = "token"

  extractPayload(rawToken: string): TokenPayload {
    return new TokenPayload(rawToken);
  }

  /**
   * Valid JWT token as an input is expected.
   */
  saveToken(rawToken: string) {
    localStorage.setItem(this.#key, rawToken);
  }

  getToken(): string | null {
    return localStorage.getItem(this.#key);
  }

  deleteToken() {
    localStorage.removeItem(this.#key);
  }

  /**
   * Returns 0 if token is missing or expired, otherwise returns time in seconds
   * during which the token is valid.
   */
  get expirationInSeconds(): number {
    const token = this.getToken();

    if (token === null) {
      return 0;
    }

    const { expiration } = this.extractPayload(token);
    const now = Math.floor(new Date().getTime() / 1000)
    return (expiration > now) ? expiration - now : 0;
  }

  get tokenIsValid(): boolean {
    const token = this.getToken();

    if (token === null) {
      return false;
    }

    const { expiration } = this.extractPayload(token);
    const now = Math.floor(new Date().getTime() / 1000);
    return expiration > now;
  }
}
