// Scene module registry (DevLog-017): every `<id>.ts` next to this file is the scene module of the showcase milestone
// `<id>` (default export: ShowcaseModule, contract in ../showcase/types.ts). Modules load lazily; a milestone with a
// spec but no module here shows no story.
import type { ShowcaseModule } from '../showcase/types';

const files = import.meta.glob<{ default: ShowcaseModule }>(['./*.ts', '!./index.ts', '!./*.test.ts']);

export const SHOWCASES: Record<string, () => Promise<ShowcaseModule>> = Object.fromEntries(
	Object.entries(files).map(([path, load]) => [path.slice(2, -3), () => load().then((m) => m.default)])
);

export const hasShowcase = (id: string): boolean => id in SHOWCASES;
