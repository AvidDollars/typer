/**
 * ingores "Shift, Caps lock, etc..." and negative indices
 */
export function discardIrrelevantKeys(event: KeyboardEvent): boolean {
  const { key } = event;

  return (
    key.length === 1 ||
    key === "Backspace" ||
    key === "Enter"
  );
}

export function extractKey(event: KeyboardEvent): string {
  return event.key;
}

/**
 * The state of typing session. To be used in "scan" operator to update typing stream.
 */
export class SessionState {

  activeTypoos = new Map<number, string>(); // Map<index, invalidChar>
  #index = -1;
  #charArray: string[] = [];
  #startTime = 0; // timestamp in miliseconds

  /**
   * #errors = {
   *    char_a: { char_b: <mistakes_count>, char_c: <mistakes_count> },
   *    char_x: { char_c: <mistakes_count>, char_d: <mistakes_count> },
   * }
   */
  #errors: Map<string, Map<string, number>> = new Map();

  markStart(): void {
    if (this.#startTime !== 0) {
      console.warn("Start of the typing session is already set to non-zero value.");
    }
    this.#startTime = new Date().getTime();
  }

  loadText(rawText: string): void {
    this.#charArray = [...rawText];
    this.#errors = new Map(this.#charArray.map(char => [char, new Map()]));
  }

  // ENTRY POINT:
  updateState(key: string): SessionState {
    const keyIsBackspace = key === "Backspace";
    let index = (keyIsBackspace) ? --this.#index : ++this.#index;
    this.#index = (index < 0) ? -1 : index; // min index: -1

    if (this.#index <= -1) {
      return this;
    };

    // It may happen that there is " " at the end of line.
    if (key === "Enter" && this.#charArray[index] === " ") {
      return this;
    };

    if (key !== this.#charArray[index] && !keyIsBackspace) {
      this.#updateErrors(key, index);
      return this;
    };

    // delete active typoos
    const indexToDel = (keyIsBackspace) ? index + 1 : index;
    this.activeTypoos.delete(indexToDel);
    return this;
  }

  get isFinished(): boolean {
    return this.#index >= this.#charArray.length - 1;
  }

  // FINAL RESULTS
  get results() {
    const endTime = new Date().getTime();
    const elapsedMs = endTime - this.#startTime;

    // only keys with mistakes are included
    const mistakes = new Map(
      [...this.#errors].filter(([_key, mistakes]) => mistakes.size > 0),
    );

    return { mistakes, elapsedMs };
  }

  /**
   * Updates "active typoos" and "errors stats" Map objects when an incorrect key is pressed.
   */
  #updateErrors(key: string, index: number): void {
    this.activeTypoos.set(index, key);
    const correctChar = this.#charArray[index];
    const charMap = this.#errors.get(correctChar) ?? new Map<string, number>();
    charMap.set(key, (charMap.get(key) ?? 0) + 1);
  }
}
