import {request as requestImport} from './request';
import {ThemeError} from './exceptions';


class Theme {
  public isInitialized = false;

  private data: object = {};
  private names: Array<string> = [];
  // for test dependency injection
  private request = requestImport;

  async initialize(name: string){
    await this.loadNames();
    await this.load(name);
    this.isInitialized = true;
  }

  getData(){
    return this.data;
  }

  getNames(){
    return this.names;
  }

  async change(name: string) {
      await this.load(name);

      const event = new CustomEvent('mxxn.theme.changed');
      dispatchEvent(event);
  }

  private async load(name: string) {
    if(name && this.names.includes(name)){
      const response = await this.request('/app/mxxn/themes/'+name);
      const responseData = await response.json();
      const data = {};

      for (const pkg in responseData){
        for (const variable in responseData[pkg]){
          const variableName = `--${pkg}-${variable.replace(/\./g, '-')}`;
          data[variableName] = responseData[pkg][variable];
        }
      }

      this.data = data;
    }
    else {
      throw new ThemeError(`The theme with name "${name}" does not exist.`);
    }
  }

  private async loadNames() {
    const response = await this.request('/app/mxxn/themes?fields=id');
    const responseData = await response.json();
    const names = [];

    for (const name of responseData){
      names.push(name.id);
    }

    this.names = names;
  }
}

export const theme = new Theme();
