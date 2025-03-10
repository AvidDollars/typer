import { TestBed } from '@angular/core/testing';

import { ColorSchemeService } from './color-scheme.service';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';

describe('ColorSchemeService', () => {
  let service: ColorSchemeService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideExperimentalZonelessChangeDetection()]
    });
    service = TestBed.inject(ColorSchemeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
