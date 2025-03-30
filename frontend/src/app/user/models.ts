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
 * Base class for /activate, /login and /register endpoints
 */
export abstract class FormObject<Raw, Out> {

  dataIsValid = false;
  dataUnchanged = false;

  abstract rawData: Raw;
  abstract get outData(): Out;
}
