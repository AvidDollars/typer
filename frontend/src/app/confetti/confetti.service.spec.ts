import { TestBed } from '@angular/core/testing';

import { ConfettiService } from './confetti.service';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';

describe('ConfettiService', () => {
  let service: ConfettiService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideExperimentalZonelessChangeDetection()]
    });
    service = TestBed.inject(ConfettiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
