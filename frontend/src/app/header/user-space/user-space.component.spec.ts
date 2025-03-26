import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';
import { UserSpaceComponent } from './user-space.component';
import { provideRouter } from '@angular/router';
import { routes } from '../../app.routes';

describe('UserSpaceComponent', () => {
  let component: UserSpaceComponent;
  let fixture: ComponentFixture<UserSpaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserSpaceComponent],
      providers: [
        provideExperimentalZonelessChangeDetection(),
        provideRouter(routes),
      ],
    })
      .compileComponents();

    fixture = TestBed.createComponent(UserSpaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
