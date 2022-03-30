
// import {dom} from '../components'
// import * as riot from 'riot'
import Icon from '../../src/components/icon.riot'


describe('Tests_for_Icon_component',function() {
  it('Initialization_with_existing_icon', function () {
    console.log(Icon)
    // expect(mxxn.test).toBe('1234');
  })
});

//     const svg = `
//       <svg>
//         <path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
//       </svg>`
//
//     const response = jasmine.createSpyObj('text', {text: svg, ok: false})
//     window.fetch = jasmine.createSpy('fetch').and.resolveTo(response)
//
//     const element = document.createElement('component')
//     const component = riot.component(Icon)
//     const icon = component(element, {'name': 'logout'})
//
//     // @ts-ignore
//     while(icon.state.isReady === false){
//       await new Promise(resolve => setTimeout(resolve, 1));
//     }
//
//     expect(element.innerHTML).toContain('11H21V13H3V11M3')
//   afterEach(function () {
//     dom.clear()
//   })
// });
//
