import {Theme} from '../src/themes'


describe('tests_for_Theme_class', () => {
  it('mxxn_theme_change_listener_added', async () => {
    /**
     * The mxxn.theme.change event listener was added.
     */
    const responseNames = new Response(
      JSON.stringify(['light', 'dark']), { status: 200, statusText: 'OK', })

    const responseTheme = new Response(
      JSON.stringify({'icon-color': '#123456'}), { status: 200, statusText: 'OK', })

    Theme.request = jasmine.createSpy('request').and.returnValues(
      responseNames, responseTheme)

    spyOn<Theme, any>(Theme.prototype, 'changeHandler')

    const theme = new Theme('name')

    await theme.isReady
    const event = new CustomEvent('mxxn.theme.change', {detail: {name: 'light'}})

    dispatchEvent(event)

    // @ts-ignore because method is private
    expect(theme.changeHandler).toHaveBeenCalled()
  })

  it('names_and_theme_loaded', async () => {
    /**
     * The names and the theme was loaded during initialization.
     */
    const responseNames = new Response(
      JSON.stringify(['light', 'dark']), { status: 200, statusText: 'OK', })

    const responseTheme = new Response(
      JSON.stringify({'icon-color': '#123456'}), { status: 200, statusText: 'OK', })

    Theme.request = jasmine.createSpy('request').and.returnValues(
      responseNames, responseTheme)

    const theme = new Theme('name')
    await theme.isReady

    // @ts-expect-error because method is private
    expect(theme.names).toEqual(['light', 'dark'])
    // @ts-expect-error because method is private
    expect(theme.data).toEqual({'icon-color': '#123456'})

  })
});
