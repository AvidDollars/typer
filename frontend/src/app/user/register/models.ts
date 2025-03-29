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
 * instance of RegFormObject to be used as the seed in rxjs "scan" operator
 */
export const regFormBase: FormObject<RegFormDataRaw> = {
  rawData: { name: "", email: "", password: { value: "", confirm: "" } },
  dataIsValid: false,
  dataUnchanged: false,
};