import { readFileSync } from 'node:fs';

export default {
  id: 'coretica',
  name: 'Coretica',
  description: 'Supply the bundled private memory instructions through the native prompt hook.',
  register(api) {
    // The web build copies the canonical skill into this distribution. Read only
    // that static file; the hook deliberately never reads its event or transcript.
    const instructions = readFileSync(new URL('./skills/coretica-memory/SKILL.md', import.meta.url), 'utf8');
    api.on('before_prompt_build', () => ({ prependSystemContext: instructions }));
  },
};
