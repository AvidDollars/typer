import { TestBed } from '@angular/core/testing';

import { TextLoaderService } from './text-loader.service';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('TextLoaderService', () => {
  let service: TextLoaderService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideExperimentalZonelessChangeDetection(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    });
    service = TestBed.inject(TextLoaderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
