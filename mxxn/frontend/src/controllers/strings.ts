import {ReactiveController, ReactiveControllerHost} from 'lit';
import {strings} from '../states/strings';


export class StringsController implements ReactiveController {
  private host: ReactiveControllerHost;
  state: object;

  constructor(host: ReactiveControllerHost) {
    this.host = host;
    host.addController(this);

  }

  hostConnected(): void{
    this.changesHandler();
    addEventListener('mxxn.strings.changed', this.changesHandler.bind(this))

  }

  private changesHandler(): void{
    this.state = strings.state;
    this.host.requestUpdate();
  }
}
