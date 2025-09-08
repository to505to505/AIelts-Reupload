import tailwindcss from '@tailwindcss/vite';
import { svelteTesting } from '@testing-library/svelte/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
	plugins: [
		imagetools(),
		sveltekit(),
		tailwindcss(),
		VitePWA({
			registerType: 'autoUpdate',
			strategies: 'generateSW',
			injectRegister: 'script',
			manifestFilename: 'manifest.json',
			manifest: {
				name: 'aiELTS - IELTS Speaking Practice',
				short_name: 'aiELTS',
				start_url: '/',
				display: 'standalone',
				background_color: '#ffffff',
				theme_color: '#2f63fe',
				icons: [
					{
						src: '/favicon.png',
						sizes: '192x192',
						type: 'image/png'
					},
					{
						src: '/favicon.png',
						sizes: '512x512',
						type: 'image/png'
					}
				]
			}
		})
	],

	test: {
		workspace: [
			{
				extends: './vite.config.ts',
				plugins: [svelteTesting()],

				test: {
					name: 'client',
					environment: 'jsdom',
					clearMocks: true,
					include: ['src/**/*.svelte.{test,spec}.{js,ts}'],
					exclude: ['src/lib/server/**'],
					setupFiles: ['./vitest-setup-client.ts']
				}
			},
			{
				extends: './vite.config.ts',

				test: {
					name: 'server',
					environment: 'node',
					include: ['src/**/*.{test,spec}.{js,ts}'],
					exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
				}
			}
		]
	},
	optimizeDeps: {
		exclude: ['@ffmpeg/ffmpeg', '@ffmpeg/core']
	}
});
