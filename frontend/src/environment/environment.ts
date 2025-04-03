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
    }
}