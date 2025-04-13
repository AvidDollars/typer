/**
 * Shape of text fetched from GET /texts/<text_id>
 */
export interface Text {
  description: string;
  id: string;
  created_at: string;
  is_public: boolean;
  name: string;
  content: string;
  added_by: string;
}
