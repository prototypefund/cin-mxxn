import {ReactiveController, ReactiveControllerHost} from 'lit';
import {theme} from '../states/theme';

interface ThemeControllerHost extends ReactiveControllerHost {
    updateTheme? (): void
}

export class ThemeController implements ReactiveController {
  private host: ThemeControllerHost;
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

    if (typeof this.host.updateTheme !== "undefined") {
      this.host.updateTheme();
    }
  }
}
