import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BlinkingCursorComponent } from './blinking-cursor.component';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';

describe('BlinkingCursorComponent', () => {
  let component: BlinkingCursorComponent;
  let fixture: ComponentFixture<BlinkingCursorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BlinkingCursorComponent],
      providers: [provideExperimentalZonelessChangeDetection()],
    })
    .compileComponents();

    fixture = TestBed.createComponent(BlinkingCursorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
