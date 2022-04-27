import {ReactiveController, ReactiveControllerHost} from 'lit';


export class MediaController implements ReactiveController {
  private host: ReactiveControllerHost;
  private mediaQueries = {
    small: window.matchMedia('(min-width: 0px)'),
    medium: window.matchMedia('(min-width: 660px)'),
    large: window.matchMedia('(min-width: 1100px)')
  }

  size: string;

  constructor(host: ReactiveControllerHost) {
    this.host = host;
    host.addController(this);

  }

  hostConnected(){
    for (const key in this.mediaQueries){
      this.mediaQueries[key].addEventListener('change', this.changesHandler.bind(this))
    }

    this.changesHandler();
  }

  changesHandler(){
    let size = null

    for (let [media, mediaQuery] of Object.entries(this.mediaQueries)){
      if (mediaQuery.matches){
        size = media
      }
    }

    if (this.size != size){
      this.size = size
      this.host.requestUpdate();
    }
  }
}
