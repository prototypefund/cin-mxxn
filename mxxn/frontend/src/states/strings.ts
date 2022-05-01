import {request as requestImport} from '../request';
import {StringsError} from '../exceptions';


export class Strings {
  private data: object = {};
  // for test dependency injection
  private request = requestImport;

  isInitialized = false;

  async initialize(name: string){
    await this.load(name);
    this.isInitialized = true;
  }

  get state() {
    return this.data;
  }

  async load(locale: string) {
    function makeObject(data, variables) {
      Object.entries(variables).forEach(([variable, value]) => {
        const parts = variable.split('.');
        let object = data;

        parts.forEach((key, i) => {
          if (i < parts.length - 1) {
            object[key] = object[key] || {};
            object = object[key];
          }
          else {
            object[key] = value;
          }
        });
      })
    }

    try {
      const response = await this.request('/app/mxxn/strings/'+locale);
      const responseData = await response.json();
      const data = {};

      Object.entries(responseData).forEach(([pkg, value]) => {
        if ((pkg === 'mxxn' || pkg === 'mxnapp') && Object.keys(value).length > 0) {
          data[pkg] = {};
          makeObject(data[pkg], value)
        }
        else if (pkg === 'mxns' && Object.keys(value).length > 0) {
          data[pkg] = {};

          Object.entries(responseData[pkg]).forEach(([mxn, value]) => {
          
            if (Object.keys(value).length > 0) {
              data[pkg][mxn] = {};
              makeObject(data[pkg][mxn], value)
            }
          });
        }
      });

      this.data = data;
      const event = new CustomEvent('mxxn.strings.changed');
      dispatchEvent(event);
    }
    catch (ex) {
      throw new StringsError(
        'An error occurred while loading the application strings.');
    }
  }
}

export const strings = new Strings();
