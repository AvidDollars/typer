import { Injectable } from '@angular/core';
import { TokenPayload } from './models';


@Injectable({
  providedIn: 'root'
})
export class JwtTokenService {

  extractPayload(rawToken: string): TokenPayload {
    return new TokenPayload(rawToken);
  }

  saveToken(rawToken: string) {
    localStorage.setItem("token", rawToken);
  }

  getToken(): string | null {
    return localStorage.getItem("token");
  }

  deleteToken() {
    localStorage.removeItem("token");
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
