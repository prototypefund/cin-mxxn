import {html, css, LitElement} from 'lit';


export class App extends LitElement {
    static styles = css`
      :host {
			  --mxxn-toolbar-background-color: #ffffff;
			  --mxxn-toolbar-shadow-color: #000000;
			  --mxxn-navbar-background-color: #3c0f60;
			  --mxxn-navbar-shadow-color: #000000;
			  --mxxn-icon-color: #0000ff;
      }

      .app-grid{
			  height: 100vh;
			  width: 100vw;
			  display: grid;
			  grid-template-rows: 1fr;
			  grid-template-columns: auto 1fr;
		  }

		  mxxn-navbar{
        background-color: var(--mxxn-navbar-background-color);
        box-shadow: -3px 0px 6px var(--mxxn-navbar-shadow-color);
		}
    `;

  render() {
    return html`
      <div class="app-grid">
		    <mxxn-navbar></mxxn-navbar>
      </div>
    `;
  }
}
