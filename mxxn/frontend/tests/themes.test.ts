import {theme} from '../src/themes'


describe('Tests for loadNames method of the Theme class.', () => {
  it('Names has been loaded and saved as array.', async () => {
    const names = [
      {
        "id": "dark"
      },
      {
        "id": "light"
      }
    ]

    const response = new Response(
      JSON.stringify(names), { status: 200, statusText: 'OK', })

    // @ts-ignore
    theme.request = jasmine.createSpy('request').and.returnValue(response)

    // @ts-ignore
    await theme.loadNames()

    // @ts-ignore
    expect(theme.names).toEqual(['dark', 'light'])
  })
});


describe('Tests for load method of the Theme class.', () => {
  it('Data has been loaded and saved as object.', async () => {
    const data = {
      mxxn: {
        'icon.color': '#0000ff'
      },
      mxns: {
        'background.color': '#ffffff'
      },
      mxnapp: {
        'color': '#000000'
      }
    }

    const response = new Response(
      JSON.stringify(data), { status: 200, statusText: 'OK', })

    // @ts-ignore
    theme.request = jasmine.createSpy('request').and.returnValue(response)

    // @ts-ignore
    await theme.load()

    // @ts-ignore
    expect(theme.data).toEqual({
      '--mxxn-icon-color': '#0000ff',
      '--mxns-background-color': '#ffffff',
      '--mxnapp-color': '#000000'
    })
  })

  fit('Data has been loaded and saved as object.', async () => {
    // @ts-ignore
    await theme.load('light')
  })
});


describe('Tests for initialize method of the Theme class.', () => {
  it('Instance was initialized.', async () => {
    const data = {
      mxxn: {
        'icon.color': '#0000ff'
      },
      mxns: {},
      mxnapp: {}
    }

    const names = [
      {
        "id": "dark"
      },
      {
        "id": "light"
      }
    ]

    const responseNames = new Response(
      JSON.stringify(names), { status: 200, statusText: 'OK', })

    const responseData = new Response(
      JSON.stringify(data), { status: 200, statusText: 'OK', })

    // @ts-ignore
    theme.request = jasmine.createSpy('request').and.returnValues(responseNames, responseData)

    // @ts-ignore
    await theme.initialize('dark')

    // @ts-ignore
    expect(theme.data).toEqual({'--mxxn-icon-color': '#0000ff'})
    // @ts-ignore
    expect(theme.names).toEqual(['dark', 'light'])
  })
});


describe('Tests for getData method of the Theme class.', () => {
  it('The data were returned.', async () => {
    const data = {
      mxxn: {
        'icon.color': '#0000ff'
      },
      mxns: {},
      mxnapp: {}
    }

    const names = [
      {
        "id": "dark"
      },
      {
        "id": "light"
      }
    ]

    const responseNames = new Response(
      JSON.stringify(names), { status: 200, statusText: 'OK', })

    const responseData = new Response(
      JSON.stringify(data), { status: 200, statusText: 'OK', })

    // @ts-ignore
    theme.request = jasmine.createSpy('request').and.returnValues(responseNames, responseData)

    await theme.initialize('dark')

    expect(theme.getData()).toEqual({'--mxxn-icon-color': '#0000ff'})
  })
});


describe('Tests for getNames method of the Theme class.', () => {
  it('The names were returned.', async () => {
    const data = {
      mxxn: {
        'icon.color': '#0000ff'
      },
      mxns: {},
      mxnapp: {}
    }

    const names = [
      {
        "id": "dark"
      },
      {
        "id": "light"
      }
    ]

    const responseNames = new Response(
      JSON.stringify(names), { status: 200, statusText: 'OK', })

    const responseData = new Response(
      JSON.stringify(data), { status: 200, statusText: 'OK', })

    // @ts-ignore
    theme.request = jasmine.createSpy('request').and.returnValues(responseNames, responseData)

    await theme.initialize('dark')

    expect(theme.getNames()).toEqual(['dark', 'light'])
  })
});


describe('Tests for change method of the Theme class.', () => {
  it('Theme data changed.', async () => {
    const dark = {
      mxxn: {
        'icon.color': '#ffffff'
      },
      mxns: {},
      mxnapp: {}
    }

    const light = {
      mxxn: {
        'icon.color': '#000000'
      },
      mxns: {},
      mxnapp: {}
    }

    const names = [
      {
        "id": "dark"
      },
      {
        "id": "light"
      }
    ]

    const responseNames = new Response(
      JSON.stringify(names), { status: 200, statusText: 'OK', })

    const responseDark = new Response(
      JSON.stringify(dark), { status: 200, statusText: 'OK', })

    const responseLight = new Response(
      JSON.stringify(light), { status: 200, statusText: 'OK', })

    // @ts-ignore
    theme.request = jasmine.createSpy('request').and.returnValues(
      responseNames, responseDark, responseLight
    )

    await theme.initialize('dark');

    expect(theme.getData()).toEqual({'--mxxn-icon-color': '#ffffff'})

    await theme.change('light');

    expect(theme.getData()).toEqual({'--mxxn-icon-color': '#000000'})
  })
});
