/**
 * Send an HTTP request to the given URL.
 *
 * The request function is essentially a mapper for fetch with some
 * default options. The options are set to match the most API calls.
 * The function also implements error handling and throws an
 * exception if an error occurs.
 *
 * @param url The URL of the request
 * @param options A options object merged into the default options
 * @returns Promise resolved with a Response, rejected with RequestError
 */
declare function request(url: string, options?: RequestInit): Promise<Response>;
export { request };
