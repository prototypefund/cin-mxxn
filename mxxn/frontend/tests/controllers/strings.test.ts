// @ts-nocheck
import {strings} from '../../src/states/strings';
import {StringsController} from '../../src/controllers/strings';
import {LitElement} from 'lit';


class StringsElement extends LitElement {
  private strings = new StringsController(this);
}

customElements.define('mxxn-strings-element', StringsElement);

describe('Tests for StringsController.', () => {
  it('The state variable updated after initialization.', async () => {
    const en = {
      mxxn: {
        'app.login': 'login'
      },
      mxns: {},
      mxnapp: {}
    };

    const response = new Response(
      JSON.stringify(en), { status: 200, statusText: 'OK', });

    strings.request = jasmine.createSpy('request').and.returnValue(response);

    const mediaElement = document.createElement('mxxn-strings-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-strings-element');
    await element.updateComplete;

    await strings.initialize();

    expect(element.strings.state).toEqual({mxxn: {app: {login: 'login'}}});

  });

  it('The state variable updated after string loading.', async () => {
    const en = {
      mxxn: {
        'app.login': 'login'
      },
      mxns: {},
      mxnapp: {}
    };

    const de = {
      mxxn: {
        'app.login': 'anmelden'
      },
      mxns: {},
      mxnapp: {}
    };

    const responseOne = new Response(
      JSON.stringify(en), { status: 200, statusText: 'OK', });

    const responseTwo = new Response(
      JSON.stringify(de), { status: 200, statusText: 'OK', });

    strings.request = jasmine.createSpy('request').and.returnValues(responseOne, responseTwo);

    const mediaElement = document.createElement('mxxn-strings-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-strings-element');
    await element.updateComplete;
    await strings.initialize();

    await strings.load('de');

    expect(element.strings.state).toEqual({mxxn: {app: {login: 'anmelden'}}});

  });

  afterEach(() => {
    document.body.innerHTML = '';
  });
});

