import { Routes } from '@angular/router';
import { LoginComponent } from './user/login/login.component';
import { RegisterComponent } from './user/register/register.component';
import { ActivateComponent } from './user/activate/activate.component';
import { ResetComponent } from './user/reset/reset.component';

// TODO: lazy loading
export const routes: Routes = [
  {
    path: "login",
    component: LoginComponent,
  },
  {
    path: "register",
    component: RegisterComponent,
  },
  {
    path: "reset",
    component: ResetComponent,
  },
  {
    path: "activate/:token",
    component: ActivateComponent,
  }
];
