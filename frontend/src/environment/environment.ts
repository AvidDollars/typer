export const environment = {
    production: false,
    BACKEND_BASE_URL: "http://localhost:8000",

    route(path: string): string {
        return `${this.BACKEND_BASE_URL}/${path}`;
    },

    get registrationUrl(): string {
      return this.route("register");
    },

    activateUrl(token: string): string {
      return this.route(`activate/${token}`);
    },

    get loginUrl(): string {
      return this.route("login");
    },

    text(textId: string): string {
      return this.route(`texts/${textId}`);
    },

    // TODO: retrieve default text based on the query: "select id from texts where is_public = true limit 1"
    // current value is hardcoded...
    get defaultTextId(): string {
      //shortest: bb461796-fe3c-4258-87ed-a3d9e4820f7a
      //normal len: f9556879-8ddb-493f-a256-1c59c4b0a523
      return "bb461796-fe3c-4258-87ed-a3d9e4820f7a";
    },

    get saveSessionUrl(): string {
      return this.route(`typing-sessions`)
    }
}