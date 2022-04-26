import {Icon} from '../../src/elements/icon'
import {IconLoadError} from '../../src/exceptions'

customElements.define('mxxn-icon', Icon);


describe('Tests for Icon component.',function() {
  beforeEach(() => {
    document.body.innerHTML = '';
  });

  it('Initialization with existing icon.', async () => {
    const svg = `
      <svg>
        <path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
      </svg>`

    const response = new Response(svg , { status: 200, statusText: 'OK', });
    Icon.request = jasmine.createSpy('request').and.returnValue(response);

    const iconElement = document.createElement('mxxn-icon');
    iconElement.setAttribute('name', 'menu');
    document.body.appendChild(iconElement);
    const icon = document.body.querySelector<Icon>('mxxn-icon');
    await icon.updateComplete;
    await icon.isLoading;

    expect(icon.shadowRoot.innerHTML).toContain('11H21V13H3V11M3');
  })

  it('Wrong initial icon name.', async () => {
    const test = async () => {
      const iconElement = document.createElement('mxxn-icon');
      iconElement.setAttribute('name', 'menu');
      document.body.appendChild(iconElement);
      const icon = document.body.querySelector<Icon>('mxxn-icon');
      await icon.updateComplete;
      await icon.isLoading;
    }

    await expectAsync(test()).toBeRejectedWithError(IconLoadError);
  })

  afterEach(() => {
    document.body.innerHTML = '';
  });
});
