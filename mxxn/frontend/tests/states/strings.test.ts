// @ts-nocheck
import {strings} from '../../src/states/strings'
import {StringsError} from '../../src/exceptions';


describe('Tests for load method of the Strings class.', () => {
  it('Nested object was created.', async () => {
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

    await strings.load();

    expect(strings.state.mxxn.app.login).toEqual('login');
  });

  it('Nested objects for MxnApp and Mxns were created.', async () => {
    const en = {
      mxxn: {
        'app.login': 'login',
        'app.logout': 'logout'
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
        'app.test.a': 'test-a',
        'app.test.b': 'test-b'
      }
    };

    const response = new Response(
      JSON.stringify(en), { status: 200, statusText: 'OK', });

    strings.request = jasmine.createSpy('request').and.returnValue(response);

    await strings.load();

    expect(strings.state.mxxn.app.login).toEqual('login');
    expect(strings.state.mxxn.app.logout).toEqual('logout');
    expect(strings.state.mxns.one.one.a).toEqual('one-a');
    expect(strings.state.mxns.one.one.b).toEqual('one-b');
    expect(strings.state.mxns.two.two.a).toEqual('two-a');
    expect(strings.state.mxns.two.two.b).toEqual('two-b');
    expect(strings.state.mxnapp.app.test.a).toEqual('test-a');
    expect(strings.state.mxnapp.app.test.b).toEqual('test-b');
  });

  it('Throw StringError.', async () => {
    await expectAsync(strings.load('en')).toBeRejectedWithError(StringsError);
  });
});


describe('Tests for initialize method of the Strings class.', () => {
  it('The isInitialized property was set.', async () => {
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

    expect(strings.isInitialized).toBeFalse()

    await strings.initialize('en');

    expect(strings.isInitialized).toBeTrue()
  });

  fit('Nested object was created.', async () => {
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

    await strings.initialize('en');

    expect(strings.state.mxxn.app.login).toEqual('login');
  });
});
