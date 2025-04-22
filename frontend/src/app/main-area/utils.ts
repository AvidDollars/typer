import { Session, TypingStats } from "../session/models";

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
  #textId = "";
  #errors: TypingStats = new Map();

  markStart(): void {
    if (this.#startTime !== 0) {
      console.warn("Start of the typing session is already set to non-zero value.");
    }
    this.#startTime = new Date().getTime();
  }

  loadText(rawText: string, textId: string): void {
    this.#charArray = [...rawText];
    this.#errors = new Map(this.#charArray.map(char => [char, new Map()]));
    this.#textId = textId;
  }

  // ENTRY POINT:
  updateState(key: string): SessionState {
    const keyIsBackspace = key === "Backspace";
    let index = (keyIsBackspace) ? --this.#index : ++this.#index;
    this.#index = (index < 0) ? -1 : index; // min index: -1
    const correctKey = this.#charArray[index];
    const enterOnEndOfLine = key === "Enter" && correctKey === " "; // It may happen that there is " " at the end of line.

    if (this.#index < -1 || enterOnEndOfLine) {
      return this;
    };

    if (key !== correctKey && !keyIsBackspace) {
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
  get results(): Session {
    const endTime = new Date().getTime();
    const duration_in_miliseconds = endTime - this.#startTime;

    // Object.fromEntries(...) -> stats must be valid JS object in order to send it to the backend.
    // only keys with mistakes are included
    const errors = new Map(
      [...this.#errors]
        .filter(([_key, mistakes]) => mistakes.size > 0)
        .map(([key, mistakes]) => [key, Object.fromEntries(mistakes)])
    );

    return { duration_in_miliseconds, text_id: this.#textId, stats: Object.fromEntries(errors) };
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
