/**
 * ingores "Shift, Caps lock, etc..." and negative indices
 */
export function discardIrrelevantKeys(event: KeyboardEvent): boolean {
  const { key } = event;
  return key.length === 1 || key === "Backspace";
}

export function extractKey(event: KeyboardEvent): string {
  return event.key;
}

/**
 * The state of typing session. To be used in "scan" operator to update of typing stream.
 */
export class SessionState {
  #index = -1;
  #charArray: string[] = [];
  #errors: Map<string, number> = new Map();

  /** TODO: nested errors:
   * errs = {
   *    char_a: { char_b: <mistakes_count>, char_c: <mistakes_count> },
   *    char_x: { char_c: <mistakes_count>, char_d: <mistakes_count> },
   * }
   */
  //errors: Map<string, Map<string, number>> = new Map();

  loadText(rawText: string) {
    this.#charArray = [...rawText];
    this.#errors = new Map(this.#charArray.map(char => [char, 0]));
  }

  // ENTRY POINT:
  updateState(key: string): SessionState {
    let index = (key === "Backspace") ? --this.#index : ++this.#index;
    this.#index = (index < 0) ? -1 : index; // min index: -1
    if (this.#index <= -1) return this;
    if (key !== this.#charArray[index]) this.#updateErrors(key, index);
    return this;
  }

  get isFinished(): boolean {
    return this.#index >= this.#charArray.length - 1;
  }

  // FINAL RESULTS
  get results() {
    return this.#errors;
  }

  #updateErrors(key: string, index: number): void {
    const correctChar = this.#charArray[index];
    const isCorrectKey = (key === correctChar);

    if (!isCorrectKey && key !== "Backspace") {
      this.#errors.set(correctChar, (this.#errors.get(correctChar) ?? 0) + 1);
    };
  }
}