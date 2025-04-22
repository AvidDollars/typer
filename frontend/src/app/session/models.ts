/**
 * #errors = {
 *    char_a: { char_b: <mistakes_count>, char_c: <mistakes_count> },
 *    char_x: { char_c: <mistakes_count>, char_d: <mistakes_count> },
 * }
 */
export type TypingStats = Map<string, Map<string, number>>;

/**
 * Shape of data for "POST /typing-sessions"
 */
export interface Session {
  duration_in_miliseconds: number;
  text_id: string;
  stats: object;
}

export interface SaveSessionResult {
  state: "saved" | "failed";
  message?: string;
}