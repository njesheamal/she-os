/** @type {import("prettier").Config} */
const config = {
	useTabs: true,
	singleQuote: true,
	trailingComma: 'none',
	printWidth: 100,
	// These plugins format Svelte syntax and Tailwind classes consistently.
	plugins: ['prettier-plugin-svelte', 'prettier-plugin-tailwindcss'],
	overrides: [{ files: '*.svelte', options: { parser: 'svelte' } }],
	// Tailwind v4 keeps its theme and utility source in this stylesheet.
	tailwindStylesheet: './src/routes/layout.css'
};

export default config;
