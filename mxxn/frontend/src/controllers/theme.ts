import {ReactiveController, ReactiveControllerHost} from 'lit';
import {theme} from '../states/theme';


export class ThemeController implements ReactiveController {
  private host: ReactiveControllerHost;
  state: object;

  constructor(host: ReactiveControllerHost) {
    this.host = host;
    host.addController(this);

  }

  hostConnected(): void{
    this.changesHandler();
    addEventListener('mxxn.theme.changed', this.changesHandler.bind(this))

  }

  private changesHandler(): void{
    this.state = theme.state;
    this.host.requestUpdate();
  }
}
