import * as riot from 'riot'
import MxxnApp from './components/app.riot'
import MxxnLogin from './components/login.riot'
import {request} from './request'

const url = '/app/mxxn/themesdd'


export async function app(){
  const mountApp = riot.component(MxxnApp)
  console.log(await request(url))
  // console.log('#############')
  mountApp(document.body)
}

export function login(){
  const mountLogin = riot.component(MxxnLogin)
  mountLogin(document.body)
}
