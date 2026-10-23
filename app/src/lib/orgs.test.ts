import { describe, expect, it } from 'vitest';
import { matches, sortOrgs } from './orgs';
import type { Org } from './types';

const org = (id: string, name: string, extra: Partial<Org> = {}): Org => ({
	id, name, type: 'company', country: '', parent: '', children: [], status: 'active', founded: '', dissolved: '',
	ror: '', qid: '', website: '', aliases: [], printed: [], links: [], events: [], lens: {}, ...extra
});

describe('org search and sort', () => {
	it('matches accents, aliases and printed strings', () => {
		const o = org('org_tu_berlin', 'Technische Universität Berlin', {
			aliases: [{ alias: 'TU Berlin', type: 'short name' }],
			printed: ['Technische Universitat Berlin']
		});
		expect(matches(o, 'universitat')).toBe(true);
		expect(matches(o, 'tu berlin')).toBe(true);
		expect(matches(o, 'eindhoven')).toBe(false);
	});
	it('sorts by lens counts, ties by name', () => {
		const a = org('a', 'B org', { lens: { pub: 5 } });
		const b = org('b', 'A org', { lens: { pub: 5 } });
		const c = org('c', 'C org', { lens: { pub: 9 } });
		expect(sortOrgs([a, b, c], 'lens.pub', 'desc').map((o) => o.id)).toEqual(['c', 'b', 'a']);
	});
});
