import { FormObject } from "../models";

/**
 * Shape of raw data from login form
 */
export interface LoginFormDataRaw {
  user: string;
  password: string;
}

/**
 * Shape of data to be sent to /login endpoint
 */
export interface LoginFormDataOut {
  name?: string;
  email?: string;
  password: string;
}

/**
 * Implementation of FormObject for /login endpoint
 */
export class LoginFormObject extends FormObject<LoginFormDataRaw, LoginFormDataOut> {

  rawData = { user: "", password: "" };

  get outData(): LoginFormDataOut {
    const { user, password } = this.rawData;
    const email = (user.includes("@")) ? user : undefined; // name cannot contain "@" character
    const name = (email === undefined) ? user : undefined;
    return { name, email, password };
  }

}