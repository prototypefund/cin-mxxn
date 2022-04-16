import {App} from './elements/app';
import {Mainbar} from './elements/mainbar';
import {Navbar} from './elements/navbar';
import {theme} from './themes'


customElements.define('mxxn-app', App);
customElements.define('mxxn-navbar', Navbar);
customElements.define('mxxn-mainbar', Mainbar);

export {
    theme
}
