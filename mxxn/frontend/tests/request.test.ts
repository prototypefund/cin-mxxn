import request from '../src/request'
import {RequestError} from '../src/exceptions'


/**
 * Tests for the request funktion
 */
describe('tests_for_request_function',function() {
  /**
   * The HTTP status code is 200.
   */
  it('status_is_200', async function () {
    const response = {status: 200}
    window.fetch = jasmine.createSpy('fetch').and.resolveTo(response)
    const url = '/app/mxxn/theme'

    const result = await request(url)

    expect(result.status).toBe(200)
  })

  /**
   * The HTTP status code is 201.
   */
  it('status_is_201', async function () {
    const response = {status: 201}
    window.fetch = jasmine.createSpy('fetch').and.resolveTo(response)
    const url = '/app/mxxn/theme'

    const result = await request(url)

    expect(result.status).toBe(201)
  })

  /**
   * The HTTP status code is 404 and error occurred.
   */
  fit('status_is_404', async function () {
    const response = {status: 404, statusText: 'Not Found'}
    window.fetch = jasmine.createSpy('fetch').and.resolveTo(response)
    const url = '/app/mxxn/theme'

    await expectAsync(request(url)).toBeRejectedWithError(RequestError, /404/);
  })
});
