/**
 * Module provides shared functionality to be used during testing phase.
 */


/**
 * To be used instead of "fakeAsync" (requires zone.js as dependency, but the project is configured in zoneless mode)
 * for waiting before next execution.
 */
export function waitMiliseconds(ms: number) {
    const start = new Date().getTime();
    let end = start;
  
    while (end < start + ms) {
      end = new Date().getTime();
    }
}