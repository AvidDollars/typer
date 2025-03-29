/**
 * Module contains commmon models for /activate, /login and /register endpoints
 */

/**
 * Result of "submit" action
 */
export interface SubmissionResult {
  state: "invalidForm" | "submitFailed" | "submitOk";
  message: string;
}

/**
 * Result of account activation (GET /activate/<activation_token>)
 */
export interface ActivationResult {
  activated: boolean;
  detail: string;
}

/**
 * Form object to be used in 'trySendRequest' method
 */
export interface FormObject<T> {
  rawData: T;
  dataIsValid: boolean;
  dataUnchanged: boolean
}