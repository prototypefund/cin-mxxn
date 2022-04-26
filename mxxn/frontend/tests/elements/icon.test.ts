import {Icon} from '../../src/elements/icon'


describe('Tests for Icon component',function() {
  fit('Initialization with existing icon', async () => {
    const svg = `
      <svg>
        <path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
      </svg>`

    const response = new Response(svg , { status: 200, statusText: 'OK', });
    Icon.request = jasmine.createSpy('request').and.returnValue(response);

    customElements.define('mxxn-icon', Icon);
    const iconElement = document.createElement('mxxn-icon');
    iconElement.setAttribute('name', 'menu');
    document.body.appendChild(iconElement);
    const icon = document.body.getElementsByTagName('mxxn-icon')[0]

    // @ts-ignore
    await icon.updateComplete;
    // @ts-ignore
    await icon.isLoading

    expect(icon.shadowRoot.innerHTML).toContain('11H21V13H3V11M3')
  })
});
