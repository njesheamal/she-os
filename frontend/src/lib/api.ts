const API_BASE = '/api';

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
	const response = await fetch(`${API_BASE}${path}`, {
		...init,
		headers: {
			Accept: 'application/json',
			...(init.headers ?? {})
		}
	});

	if (!response.ok) {
		let detail = '';
		try {
			const payload = (await response.json()) as { detail?: string };
			detail = payload.detail ? `: ${payload.detail}` : '';
		} catch {
			// Error responses may not contain JSON.
		}

		throw new Error(`Request to ${path} failed with ${response.status}${detail}`);
	}

	return (await response.json()) as T;
}

export type BrandStatus = 'active' | 'inactive';
export type FieldNoteStatus = 'draft' | 'published' | 'archived' | 'scheduled';

export interface Brand {
	id: string;
	slug: string;
	name: string;
	description?: string | null;
	status: BrandStatus;
	created_at: string;
	updated_at: string;
}

export interface FieldNote {
	id: string;
	title: string;
	slug?: string;
	status: FieldNoteStatus;
	description?: string | null;
	theme?: string | null;
	excerpt?: string | null;
	tags?: string[];
	created_at: string;
	updated_at: string;
}

export async function getBrands(): Promise<Brand[]> {
	return request<Brand[]>('/brands');
}

export async function getPublishedFieldNotes(): Promise<FieldNote[]> {
	return request<FieldNote[]>('/field-notes?status=published');
}
