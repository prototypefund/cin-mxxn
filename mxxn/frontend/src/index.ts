import * as riot from 'riot'
import {request} from './request'
import MxxnApp from './components/app.riot'
import MxxnLogin from './components/login.riot'


function app(){
  const mountApp = riot.component(MxxnApp)
  mountApp(document.body)
}

function login(){
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
