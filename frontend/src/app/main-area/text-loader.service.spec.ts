import { TestBed } from '@angular/core/testing';

import { TextLoaderService } from './text-loader.service';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';

describe('TextLoaderService', () => {
  let service: TextLoaderService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideExperimentalZonelessChangeDetection(),
      ]
    });
    service = TestBed.inject(TextLoaderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
