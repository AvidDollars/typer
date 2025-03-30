import { FormObject } from "../models";

/**
 * Shape of raw data from registration form
 */
export interface RegFormDataRaw {
  name: string;
  email: string;
  password: {
    value: string;
    confirm: string;
  }
}

/**
 * Shape of data to be sent to /register endpoint
 */
export interface RegFormDataOut {
  name: string;
  email: string;
  password: string;
}

/**
 * Implementation of FormObject for /register endpoint
 */
export class RegFormObject extends FormObject<RegFormDataRaw, RegFormDataOut> {

  rawData = { name: "", email: "", password: { value: "", confirm: "" } };

  get outData(): RegFormDataOut {
    const { name, email, password: { value } } = this.rawData;
    return { name, email, password: value };
  }

}