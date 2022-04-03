declare class RequestError extends Error {
    constructor(message: string);
}
declare class IconLoadError extends Error {
    constructor(message: string);
}
export { RequestError, IconLoadError };
