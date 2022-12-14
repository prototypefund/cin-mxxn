import {html, css, LitElement} from 'lit';
import {state} from 'lit/decorators.js';
import {theme} from '../states/theme';
import {strings} from '../states/strings';
import {MediaController} from '../controllers/media';
import {StringsController} from '../controllers/strings';
import {ThemeController} from '../controllers/theme';


export class App extends LitElement {
  private media = new MediaController(this);
  private strings = new StringsController(this);
  private theme = new ThemeController(this);

  @state()
  private isInitialized = false;

  constructor() {
    super();
    this.initialize()
  }

  async initialize() {
    await theme.initialize('light');
    await strings.initialize('de');
    this.isInitialized = true;
  }

  updateTheme(){
    for (const variable in this.theme.state){
      this.style.setProperty(variable, this.theme.state[variable]);
    }
  }

  changeTheme(){
    theme.load('dark');
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

    mxxn-navbar{
      min-width: 200px;
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

            <div>
              mxns
            </div>
          </div>
        </div>
      `;
    }
  }
}
