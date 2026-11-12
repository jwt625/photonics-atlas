<script lang="ts">
	// History tab display / text faces (DevLog-017 D997), self-hosted in static/fonts with their OFL license texts.
	// Playfair Display ships unmodified (its OFL reserves the name); Source Serif 4 is instanced (wght 400-600, no opsz
	// axis) and subset to Latin, Latin Extended-A, Greek, punctuation, super / subscripts, arrows and a few math signs.
	// Declared here (history route only) with base-path aware URLs; the two upright faces are preloaded, italics load
	// only when used.
	import { staticUrl } from '../paths';

	const u = (f: string) => staticUrl(`fonts/${f}`);
	const css = `
@font-face{font-family:"Playfair Display";src:url("${u('PlayfairDisplay.woff2')}") format("woff2");font-weight:400 900;font-style:normal;font-display:swap}
@font-face{font-family:"Playfair Display";src:url("${u('PlayfairDisplay-Italic.woff2')}") format("woff2");font-weight:400 900;font-style:italic;font-display:swap}
@font-face{font-family:"Source Serif 4";src:url("${u('SourceSerif4.woff2')}") format("woff2");font-weight:400 600;font-style:normal;font-display:swap;size-adjust:96%}
@font-face{font-family:"Source Serif 4";src:url("${u('SourceSerif4-Italic.woff2')}") format("woff2");font-weight:400 600;font-style:italic;font-display:swap;size-adjust:96%}`;
</script>

<svelte:head>
	<link rel="preload" href={u('PlayfairDisplay.woff2')} as="font" type="font/woff2" crossorigin="anonymous" />
	<link rel="preload" href={u('SourceSerif4.woff2')} as="font" type="font/woff2" crossorigin="anonymous" />
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html `<style>${css}</style>`}
</svelte:head>
