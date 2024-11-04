import { TestBed } from '@angular/core/testing';
import { JwtTokenService } from './jwt.token.service';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';
import { waitMiliseconds } from '../shared/testing';

/**
 * Provides JWT token for testing purposes.
 * "expirationInSeconds" to be provided as an input which marks token's validity period in seconds
 * from the time token was created.
 */
function getJwtToken(config: { expirationSeconds: number }): string {
  const expiration = Math.floor(new Date().getTime() / 1000) + Math.floor(config.expirationSeconds);

  let payload = JSON.stringify({
    "role": "1",
    "id": "d9c4441c-929c-4e3f-ad70-e1d58b3a6669",
    "exp": expiration,
  });

  payload = payload.replace(/-/g, '+').replace(/_/g, '/');
  payload = btoa(payload);

  const token = `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.${payload}.p3w-dYNmvQ5etRkpgPu7dLPj-_QD1gUH99CUBBvtV5A`;
  return token;
}

describe('JwtTokenService', () => {
  let service: JwtTokenService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideExperimentalZonelessChangeDetection()]
    });
    service = TestBed.inject(JwtTokenService);
    service.deleteToken();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should extract payload from raw token', () => {
    const rawToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiMSIsImlkIjoiZDljNDQ0MWMtOTI5Yy00ZTNmLWFkNzAtZTFkNThiM2E2NjY5IiwiZXhwIjoxNzMwNzM1OTA4fQ.XkQlPKjvoLW1nzj7pX_b2etW_Sg9b99Fp8dJkMgJVp0";
    const { role, id, expiration } = service.extractPayload(rawToken);

    expect(role).toBe("1");
    expect(id).toBe("d9c4441c-929c-4e3f-ad70-e1d58b3a6669");
    expect(expiration).toBe(1730735908);
  });

  it('should return expiration=0 for present but expired token', () => {
    service.saveToken("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiMSIsImlkIjoiZDljNDQ0MWMtOTI5Yy00ZTNmLWFkNzAtZTFkNThiM2E2NjY5IiwiZXhwIjoxNzMwNzM1OTA4fQ.XkQlPKjvoLW1nzj7pX_b2etW_Sg9b99Fp8dJkMgJVp0");
    const token = service.getToken();
    expect(token).not.toBeNull();
  });

  it('should return expiration=0 for missing token', () => {
    const token = service.getToken();
    expect(token).toBeNull();
    const expiration = service.expirationInSeconds;
    expect(expiration).toBe(0);
  })

  it('should return expiration>50 && expiration<60 for not-expired token with expiration set to 60 seconds from now and mark token validity correctly', () => {
    let token = service.getToken();
    expect(token).toBeNull();
    expect(service.tokenIsValid).toBeFalse();

    const freshToken = getJwtToken({ expirationSeconds: 60 });
    service.saveToken(freshToken);
    token = service.getToken();
    expect(token).not.toBeNull();
    expect(service.tokenIsValid).toBeTrue();

    expect(service.expirationInSeconds).toBeGreaterThan(50);
    waitMiliseconds(1100);
    expect(service.expirationInSeconds).toBeLessThan(60);
  })

  it('should return expiration<0 for the token at first, then should mark token as invalid after the expiration', () => {
    let token = service.getToken();
    expect(token).toBeNull();
    expect(service.tokenIsValid).toBeFalse();

    const freshToken = getJwtToken({ expirationSeconds: 1 });
    service.saveToken(freshToken);
    token = service.getToken();
    expect(token).not.toBeNull();
    expect(service.tokenIsValid).toBeTrue();

    expect(service.expirationInSeconds).toBeGreaterThan(0);
    waitMiliseconds(1100);
    expect(service.expirationInSeconds).toBe(0);
    expect(service.tokenIsValid).toBeFalse();
  })
});
