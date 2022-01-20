import { nodeResolve } from '@rollup/plugin-node-resolve';
import typescript from '@rollup/plugin-typescript';


export default {
	input: 'src/ts/mxxn.ts',
  	output: {
		name: 'mxxn',
    		file: 'static/js/mxxn.js',
    		format: 'iife'
  	},
	plugins: [
		typescript(),
		nodeResolve()
	]
};
