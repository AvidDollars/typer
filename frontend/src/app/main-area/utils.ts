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
