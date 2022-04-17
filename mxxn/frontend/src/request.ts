/**
 * The request module contains functions for handling API calls.
 */
import {RequestError} from './exceptions';


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
async function request(url: string, options: RequestInit = {}): Promise<Response>{
  const defaultOptions: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
  };

  const usedOptions = {...defaultOptions, ...options};

  const response = await fetch(url, usedOptions);
  const status = response.status;

  if (status === 200 || status === 201) {
    return response;
  }

  const message = `
    An error occurred during the call of the URL ${url}.
    Status: ${status} ${response.statusText}
    `;

  throw new RequestError(message);
}


export {
  request
};

