import { JwtTokenService } from './jwt.token.service';
import { HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';

/**
 * If JWT token is valid, it will be added for each HTTP request
 */
export function authInterceptor(request: HttpRequest<unknown>, next: HttpHandlerFn) {
  const jwtService = inject(JwtTokenService);

  if (jwtService.tokenIsValid) {
    request = request.clone({
      headers: request.headers.append("Authorization", `Bearer ${jwtService.getToken()!}`)
    });
  }

  return next(request);
}