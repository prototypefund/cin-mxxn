// @ts-nocheck
import {theme} from '../src/themes';
import {ThemeError} from '../src/exceptions';


describe('Tests for load method of the Theme class.', () => {
  it('The Mxxn variables generated.', async () => {
    const light = {
      mxxn: {
        'icon.color': '#ffffff'
      },
      mxns: {
      },
      mxnapp: {}
    };

    const response = new Response(
      JSON.stringify(light), { status: 200, statusText: 'OK', });

    theme.request = jasmine.createSpy('request').and.returnValue(response);

    await theme.load('light');

    expect(theme.state).toEqual({'--mxxn-icon-color': '#ffffff'});
  });

  it('Variables for MxnApp and Mxns were created.', async () => {
    const light = {
      mxxn: {
        'icon.color': '#ffffff',
        'icon.background.color': '#000000'
      },
      mxns: {
        one: {
          'one.a': 'one-a',
          'one.b': 'one-b'
        },
        two: {
          'two.a': 'two-a',
          'two.b': 'two-b'
        },
      },
      mxnapp: {
        'some.color': '#ff0000',
      }
    };

    const response = new Response(
      JSON.stringify(light), { status: 200, statusText: 'OK', });

    theme.request = jasmine.createSpy('request').and.returnValue(response);

    await theme.load();

    expect(theme.state).toEqual({
      '--mxxn-icon-color': '#ffffff',
      '--mxxn-icon-background-color': '#000000',
      '--mxns-one-one-a': 'one-a',
      '--mxns-one-one-b': 'one-b',
      '--mxns-two-two-a': 'two-a',
      '--mxns-two-two-b': 'two-b',
      '--mxnapp-some-color': '#ff0000'
    });
  });

  it('Throw ThemeError.', async () => {
    await expectAsync(theme.load('light')).toBeRejectedWithError(ThemeError);
  });
});


describe('Tests for initialize method of the Theme class.', () => {
  it('The isInitialized property was set.', async () => {
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

    expect(theme.isInitialized).toBeFalse()

    await theme.initialize('light');

    expect(theme.isInitialized).toBeTrue()
  });

  it('Variables were created.', async () => {
    const light = {
      mxxn: {
        'icon.color': '#ffffff'
      },
      mxns: {
      },
      mxnapp: {}
    };

    const response = new Response(
      JSON.stringify(light), { status: 200, statusText: 'OK', });

    theme.request = jasmine.createSpy('request').and.returnValue(response);

    await theme.initialize('light');

    expect(theme.state).toEqual({'--mxxn-icon-color': '#ffffff'});
  });
});
