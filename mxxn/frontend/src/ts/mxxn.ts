import * as riot from 'riot'
import MxxnApp from '../components/app.riot'
import MxxnLogin from '../components/login.riot'


export function app(){
  const mountApp = riot.component(MxxnApp)
  mountApp(document.body)
}

export function login(){
  const mountLogin = riot.component(MxxnLogin)
  mountLogin(document.body)
}
