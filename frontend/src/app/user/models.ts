/**
 * Shape of raw data from registration form
 */
export interface IRegFormDataRaw {
  name: string;
  email: string;
  password: {
    value: string;
    confirm: string;
  }
}

/**
 * Shape of data for sending "POST /register" request
 */
export interface IRegFormDataOut {
  name: string;
  email: string;
  password: string;
}

/**
 * Result of "submit" action
 */
export interface SubmissionResult {
  state: "invalidForm" | "submitFailed" | "submitOk";
  message: string;
}

/**
 * Form object to be used in 'trySendRequest' method
 */
export interface RegFormObject {
  rawData: IRegFormDataRaw;
  dataIsValid: boolean;
  dataUnchanged: boolean
}

/**
 * instance of RegFormObject to be used as the seed in rxjs "scan" operator
 */
export const regFormBase: RegFormObject = {
  rawData: { name: "", email: "", password: { value: "", confirm: "" } },
  dataIsValid: false,
  dataUnchanged: false,
};
