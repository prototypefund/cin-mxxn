import { nodeResolve } from '@rollup/plugin-node-resolve';
import typescript from 'rollup-plugin-typescript2';
import riot from 'rollup-plugin-riot'


export default {
	input: 'src/index.ts',
  	output: {
		name: 'mxxn',
    		file: 'static/js/mxxn.js',
    		format: 'iife'
  	},
	plugins: [
		nodeResolve(),
		riot(),
		typescript({
			include: [
				'src/**/*.ts+(|x)',
				'src/**/*.ts+(|x)',
				'src/**/*.riot'
			]
		}),
	]
};

