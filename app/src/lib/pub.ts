// Publication records served with every view (DevLog-010 D199g, D199h): title, venue, year, publication type in plain
// words, link (URL / DOI / arXiv), sibling-atlas page for EO / packaging papers. Source ids are join keys only.
export interface Pub {
	title?: string;
	venue?: string;
	year?: string;
	type?: string;
	url?: string;
	doi?: string;
	arxiv?: string;
	/** [site name, href] of the paper's page in a sibling atlas */
	atlas?: [string, string];
}

/** "venue, year" (either may be missing). */
export const venueYear = (p: Pub | undefined): string => [p?.venue, p?.year].filter(Boolean).join(', ');

/** Tooltip lines of a publication, optionally with the locator of a value in it. */
export function pubTip(p: Pub | undefined, locator = ''): string {
	if (!p) return '';
	return [p.title, venueYear(p), p.type, p.doi && 'DOI ' + p.doi, p.arxiv && 'arXiv ' + p.arxiv, locator && 'location: ' + locator].filter(Boolean).join('\n');
}

/** Provenance of an affiliation observation in plain words (grade code A / B is never shown, D199k). */
export function provenance(grade: string): string {
	return grade === 'A' ? 'affiliation printed in the publication' : grade === 'B' ? 'affiliation from the conference program listing' : 'affiliation';
}
