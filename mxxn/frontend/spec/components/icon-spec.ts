import {dom} from '../components'
import * as riot from 'riot'
import Icon from '../../src/components/icon.riot'


describe('Tests for the Icon component',function() {
  beforeEach(function () {
    dom.create()
  })

  it('Name state set with property', function () {
    const element = document.createElement('component')
    const component = riot.component(Icon)(element, {'name': 'logout'})

    expect(component.state['name']).toBe('static/mxxn/icons/logout.svg')
  })

  it('Name State rendered', function () {
    const element = document.createElement('component')
    riot.component(Icon)(element, {'name': 'logout'})

    expect(element.innerHTML).toContain('src="static/mxxn/icons/logout.svg"')
  })
  
  it('Name State updated', function () {
    const element = document.createElement('component')
    const component = riot.component(Icon)(element, {'name': 'logout'})
    // @ts-ignore
    component.setName('menu')

    expect(element.innerHTML).toContain('src="static/mxxn/icons/menu.svg"')
  })
  afterEach(function () {
    dom.clear()
  })
});

