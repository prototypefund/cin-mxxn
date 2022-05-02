// @ts-nocheck
import {theme} from '../../src/states/theme';
import {ThemeController} from '../../src/controllers/theme';
import {LitElement} from 'lit';


class ThemeElement extends LitElement {
  private theme = new ThemeController(this);
}

customElements.define('mxxn-theme-element', ThemeElement);

describe('Tests for StringsController.', () => {
  it('The state variable updated after initialization.', async () => {
    const light = {
      mxxn: {
        'icon.color': '#ffffff'
      },
      mxns: {},
      mxnapp: {}
    };

    const response = new Response(
      JSON.stringify(light), { status: 200, statusText: 'OK', });

    theme.request = jasmine.createSpy('request').and.returnValue(response);

    const mediaElement = document.createElement('mxxn-theme-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-theme-element');
    await element.updateComplete;

    await theme.initialize();

    expect(element.theme.state).toEqual({'--mxxn-icon-color': '#ffffff'});
  });

  it('The state variable updated after string loading.', async () => {
    const light = {
      mxxn: {
        'icon.color': '#ffffff'
      },
      mxns: {},
      mxnapp: {}
    };

    const dark = {
      mxxn: {
        'icon.color': '#000000'
      },
      mxns: {},
      mxnapp: {}
    };

    const responseOne = new Response(
      JSON.stringify(light), { status: 200, statusText: 'OK', });

    const responseTwo = new Response(
      JSON.stringify(dark), { status: 200, statusText: 'OK', });

    theme.request = jasmine.createSpy('request').and.returnValues(responseOne, responseTwo);

    const mediaElement = document.createElement('mxxn-theme-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-theme-element');
    await element.updateComplete;
    await theme.initialize();

    await theme.load('de');

    expect(element.theme.state).toEqual({'--mxxn-icon-color': '#000000'});

  });

  afterEach(() => {
    document.body.innerHTML = '';
  });
});
