import {html, css, LitElement} from 'lit';


export class Mainbar extends LitElement {
    static styles = css`
      :host {
        display: grid;
        grid-template-columns: auto auto;
      }

      mxxn-icon:hover {
        --mxxn-icon-color: #ff0000;
      }

      mxxn-icon {
        /* background-color: #990099; */
        /* heigth: 15px; */
        margin: 9px;
      }

      .left {
        display: grid;
        justify-content: left;
        grid-template-columns: auto auto;
        /* background-color: #ff0000; */
      }

      .right {
        display: grid;
        justify-content: right;
        /* background-color: #0000ff; */
      }
    `;

  render() {
    return html`
      <div class='left'>
        <mxxn-icon name='menu'></mxxn-icon>
      </div>
      <div class='right'>
        <mxxn-icon name='login'></mxxn-icon>
      </div>
    `;
  }
}
