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

    .toolbar-mxns-grid{
      display: grid;
      overflow: hidden;
      grid-template-columns: 1fr;
      grid-template-rows: 40px 1fr;
    }

    mxxn-mainbar{
      background-color: var(--mxxn-toolbar-background-color);
      box-shadow: 0px -3px 6px var(--mxxn-toolbar-shadow-color);
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
		    <div class="toolbar-mxns-grid">
          <mxxn-mainbar>
          </mxxn-mainbar>

          <div>
            mxns
          </div>
		</div>
      </div>
    `;
  }
}
