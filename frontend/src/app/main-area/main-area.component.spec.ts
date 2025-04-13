import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainAreaComponent } from './main-area.component';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('MainAreaComponent', () => {
  let component: MainAreaComponent;
  let fixture: ComponentFixture<MainAreaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainAreaComponent],
      providers: [
        provideExperimentalZonelessChangeDetection(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainAreaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
