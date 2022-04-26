import {css, LitElement} from 'lit';
import {property, state} from 'lit/decorators.js';
import {request} from 'request';
import {IconLoadError} from '../exceptions';


export class Icon extends LitElement {
  static request = request;

  @property()
  name = '';
  isLoading: Promise<void>;

  @state()
  private _svg: SVGSVGElement;

  willUpdate(changedProperties: Map<string, any>): void {

    if (changedProperties.has('name')){
      this.isLoading = this.load();
    }
  }

  async load(): Promise<void> {
    try {
      const url = 'static/mxxn/icons/' + this.name +'.svg';
      const response = await Icon.request(url, {cache: 'force-cache'});
      const text = await response.text();
      const parser = new window.DOMParser();
      const parsed = parser.parseFromString(text, 'text/html');
      this._svg = parsed.querySelector('svg');
    }
    catch (ex) {
      throw new IconLoadError(ex.message);
    }
  }

  static styles = css`
    :host {
      display: grid;
      justify-content: center;
      align-items: center;
    }

  	svg {
			fill: var(--mxxn-icon-color);
      height: 100%;
      width: auto;
		}
  `;

  render() {
    return this._svg;
  }
}
