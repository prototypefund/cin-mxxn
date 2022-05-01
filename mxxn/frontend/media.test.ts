// @ts-nocheck
import {MediaController} from '../../src/controllers/media';
import {LitElement} from 'lit';


class MediaElement extends LitElement {
  private media = new MediaController(this);
}

customElements.define('mxxn-media-element', MediaElement);

describe('Tests for changesHandler method of the MediaController.', () => {
  it('Is a small device.', async () => {
    const mediaElement = document.createElement('mxxn-media-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-media-element');
    await element.updateComplete;

    spyOnProperty(element.media.mediaQueries.small, 'matches').and.returnValue(true)
    spyOnProperty(element.media.mediaQueries.medium, 'matches').and.returnValue(false)
    spyOnProperty(element.media.mediaQueries.large, 'matches').and.returnValue(false)

    element.media.mediaQueries.small.dispatchEvent(new Event('change'))

    expect(element.media.size).toEqual('small')
  });

  it('Is a medium size device.', async () => {
    const mediaElement = document.createElement('mxxn-media-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-media-element');
    await element.updateComplete;

    spyOnProperty(element.media.mediaQueries.small, 'matches').and.returnValue(true)
    spyOnProperty(element.media.mediaQueries.medium, 'matches').and.returnValue(true)
    spyOnProperty(element.media.mediaQueries.large, 'matches').and.returnValue(false)

    element.media.mediaQueries.small.dispatchEvent(new Event('change'))

    expect(element.media.size).toEqual('medium')
  });

  it('Is a large size device.', async () => {
    const mediaElement = document.createElement('mxxn-media-element');
    document.body.appendChild(mediaElement);
    const element = document.body.querySelector('mxxn-media-element');
    await element.updateComplete;

    spyOnProperty(element.media.mediaQueries.small, 'matches').and.returnValue(true)
    spyOnProperty(element.media.mediaQueries.medium, 'matches').and.returnValue(true)
    spyOnProperty(element.media.mediaQueries.large, 'matches').and.returnValue(true)

    element.media.mediaQueries.small.dispatchEvent(new Event('change'))

    expect(element.media.size).toEqual('large')
  });

  afterEach(() => {
    document.body.innerHTML = '';
  });
});

