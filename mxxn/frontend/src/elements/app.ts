import {html, css, LitElement} from 'lit';
import {theme} from '../themes';
import {strings} from '../states/strings';
import {MediaController} from '../controllers/media';


export class App extends LitElement {
  private media = new MediaController(this);

  constructor() {
    super();

    theme.initialize('light').then(() => {
      this.updateTheme();
    });

    strings.initialize('de').then(() => {
      console.log(strings.state);
    });
  }

  connectedCallback() {
    super.connectedCallback();
    window.addEventListener('mxxn.theme.changed', this.updateTheme.bind(this));
  }

  disconnectedCallback() {
    window.removeEventListener('mxxn.theme.changed', this.updateTheme);
    super.disconnectedCallback();
  }

  updateTheme(){
    const data = theme.getData();

    for (const variable in data){
      this.style.setProperty(variable, data[variable]);
    }
  }

  changeTheme(){
    theme.change('dark');
  }

  static styles = css`
    .app-grid{
      height: 100vh;
      width: 100vw;
      display: grid;
      grid-template-rows: 1fr;
      grid-template-columns: auto 1fr;
    }

    .mainbar-mxns-grid{
      display: grid;
      overflow: hidden;
      grid-template-columns: 1fr;
      grid-template-rows: 40px 1fr;
    }

    mxxn-mainbar{
      background-color: var(--mxxn-toolbar-background-color);
      box-shadow: 0px -3px 6px var(--mxxn-toolbar-shadow-color);
    }

    mxxn-mainbar.small{
      background-color: #ff0000;
    }

    mxxn-mainbar.medium{
      background-color: #00ff00;
    }

    mxxn-mainbar.large{
      background-color: #0000ff;
    }

    mxxn-navbar{
      background-color: var(--mxxn-navbar-background-color);
      box-shadow: -3px 0px 6px var(--mxxn-navbar-shadow-color);
    }
    `;

  render() {
    return html`
      <div class="app-grid">
		    <mxxn-navbar @click="${this.changeTheme}"></mxxn-navbar>
		    <div class="mainbar-mxns-grid">
          <mxxn-mainbar class="${this.media.size}">
          </mxxn-mainbar>

          ${this.media.size}

          <div>
            mxns
          </div>
        </div>
      </div>
    `;
  }
}
