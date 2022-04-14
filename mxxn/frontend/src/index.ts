import * as riot from 'riot'
import {request} from './request'
import MxxnApp from './components/app.riot'
import MxxnLogin from './components/login.riot'
import {Theme} from './themes'


async function app(){
  const theme = new Theme('light')
  await theme.isReady

  const mountApp = riot.component(MxxnApp)
  mountApp(document.body)
}

async function login(){
  const mountLogin = riot.component(MxxnLogin)
  mountLogin(document.body)
}

namespace components {
}

export {
  request,
  app,
  login,
  components
}
