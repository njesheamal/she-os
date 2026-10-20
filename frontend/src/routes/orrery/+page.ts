import { redirect } from '@sveltejs/kit';

// Preserve old deep links by sending them to the new orrery landing page.
export function load() {
	redirect(307, '/');
}
