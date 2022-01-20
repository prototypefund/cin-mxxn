import * as riot from 'riot'
import MxxnApp from '../components/app.riot'


const mountApp = riot.component(MxxnApp)

const app = mountApp(document.body)

export default app


