/**
 * Represents payload extracted from JWT token.
 */
export class TokenPayload {

    role: string;
    id: string;
    expiration: number;

    constructor(token: string) {
        const payload = token.split(".")[1];
        const { role, id, exp } = JSON.parse(atob(payload));
        this.role = role;
        this.id = id;
        this.expiration = exp;
    }
};
