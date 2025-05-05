import { signal } from '@angular/core';
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
  allowResubmit = signal(false); // to allow form re-submission if status_code === 500

  abstract rawData: Raw;
  abstract get outData(): Out; // takes raw data and creates an object to be sent in HTTP request
}
