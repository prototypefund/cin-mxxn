
declare namespace mxxn {
    function request(url: string, options?: RequestInit): Promise<Response>;
    function app(): void;
    function login(): void;

    namespace components {
    }
}
