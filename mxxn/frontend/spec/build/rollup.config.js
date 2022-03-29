import { nodeResolve } from '@rollup/plugin-node-resolve';
import typescript from 'rollup-plugin-typescript2';
import riot from 'rollup-plugin-riot'


export default {
	input: 'spec/build/test.ts',
  	output: {
		name: 'mxxn',
    		file: 'spec/build/bundle.js',
    		format: 'iife'
  	},
	plugins: [
		nodeResolve(),
		riot(),
		typescript({
			include: [
        'spec/build/*.ts',
				'src/**/*.ts',
				'src/**/*.ts',
				'src/**/*.riot'
			]
		}),
	]
};

