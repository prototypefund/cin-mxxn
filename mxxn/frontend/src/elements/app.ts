import {html, css, LitElement} from 'lit';
import {state} from 'lit/decorators.js';
import {theme} from '../themes';
import {strings} from '../states/strings';
import {MediaController} from '../controllers/media';
import {StringsController} from '../controllers/strings';


export class App extends LitElement {
  private media = new MediaController(this);
  private strings = new StringsController(this);

  @state()
  private isInitialized = false;

  constructor() {
    super();
    this.initialize()
  }

  async initialize() {
    await theme.initialize('light');
    this.updateTheme();
    await strings.initialize('de');
    this.isInitialized = true;
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

  changeStrings(){
    strings.load('en');
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
    if (this.isInitialized) {
      return html`
        <div class="app-grid">
          <mxxn-navbar @click="${this.changeTheme}"></mxxn-navbar>
          <div class="mainbar-mxns-grid">
            <mxxn-mainbar @click='${this.changeStrings}' class="${this.media.size}">
            </mxxn-mainbar>

            ${this.media.size} <br>

            ${// @ts-ignore
              this.strings.state.mxxn.login}
            <div>
              mxns
            </div>
          </div>
        </div>
      `;
    }
  }
}
