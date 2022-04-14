import {request as requestImport} from './request'


class Theme {
  public isReady: Promise<boolean>
  private names: Array<string>
  private data: object
  // for test dependency injection
  static request = requestImport

  constructor(name: string) {
    this.isReady = new Promise((resolve) => {
      this.loadNames().then(() => {
        this.load(name).then(() => {
          addEventListener(
            'mxxn.theme.change', this.changeHandler.bind(this))
          resolve(true)
        })
      })
    });
  }

  private async load(name: string) {
    const response = await Theme.request('/app/mxxn/themes/'+name)
    const data = await response.json()

    this.data = data
  }

  private async loadNames() {
    const response = await Theme.request('/app/mxxn/themes?fields=id')
    const names = await response.json()

    this.names = names
  }

  private async changeHandler(event: CustomEvent) {
    const name = event.detail.name

    if(name && this.names.includes(name)){
      await this.load(name)

      return
    }

    throw new Error()
  }
}


export {
  Theme
}



//
// class Media{
//   media: string = 'small'
//
//   mediaQueries = {
//     small: window.matchMedia('(min-width: 320px)'),
//     medium: window.matchMedia('(min-width: 660px)'),
//     large: window.matchMedia('(min-width: 1100px)')
//   }
//
//   rootComponent = null
//   components = []
//
//   constructor() {
//     for (const key in this.mediaQueries){
//         this.mediaQueries[key].addEventListener('change', this.changesHandler)
//     }
//     this.update(false)
//   }
//
//   addRootComponent = (component) => {
//     this.components.push(component)
//     this.rootComponent = component
//     component.state.media = 'media-' + this.media
//   }
//
//   addComponent = (component) => {
//     this.components.push(component)
//     component.state.media = 'media-' + this.media
//   }
//
//   updateComponents = () => {
//     for (const component of this.components){
//       component.state.media = 'media-' + this.media
//     }
//
//     // TODO: check if rootComponent
//     this.rootComponent.update()
//   }
//
//   update = (updateComponents=true) => {
//     let size = null
//
//     for (let [media, mediaQuery] of Object.entries(this.mediaQueries)){
//       if (mediaQuery.matches){
//         size = media
//       }
//     }
//
//     if (this.media != size){
//       this.media = size
//
//       if (updateComponents) {
//         this.updateComponents()
//       }
//     }
//   }
//
//   changesHandler = () => {
//     this.update()
//   }
// }
//
// const media = new Media()
//
// function mediaPlugin(component){
//   if (component.rootComponent){
//       media.addRootComponent(component)
//   }
//   else if (component.plugins){
//     if (component.plugins.includes('media')){
//       media.addComponent(component)
//     }
//   }
// }
//
//
