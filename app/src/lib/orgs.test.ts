import { describe, expect, it } from 'vitest';
import { matches, sortOrgs } from './orgs';
import type { Org } from './types';

const org = (id: string, name: string, extra: Partial<Org> = {}): Org => ({
	id, name, type: 'company', country: '', parent: '', children: [], status: 'active', founded: '', dissolved: '',
	ror: '', qid: '', website: '', name_basis: 'eo_atlas', name_source: '', origin: ['eo'], aliases: [], rows: {},
	printed: [], events: [], notes: '', ...extra
});

describe('org search and sort', () => {
	it('matches accents, aliases and printed strings', () => {
		const o = org('org_tu_berlin', 'Technische Universität Berlin', {
			aliases: [{ alias: 'TU Berlin', type: 'short_name', scope: '' }],
			printed: [{ corpus: 'ofc2026', printed: 'Technische Universitat Berlin', n: 3, basis: 'name' }]
		});
		expect(matches(o, 'universitat')).toBe(true);
		expect(matches(o, 'tu berlin')).toBe(true);
		expect(matches(o, 'eindhoven')).toBe(false);
	});
	it('sorts by per-corpus row counts, ties by name', () => {
		const a = org('a', 'B org', { rows: { ofc2026: 5 } });
		const b = org('b', 'A org', { rows: { ofc2026: 5 } });
		const c = org('c', 'C org', { rows: { ofc2026: 9 } });
		expect(sortOrgs([a, b, c], 'rows.ofc2026', 'desc').map((o) => o.id)).toEqual(['c', 'b', 'a']);
	});
});
