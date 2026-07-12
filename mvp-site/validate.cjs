const fs = require('fs');
const matter = require('gray-matter');
const { z } = require('zod');

const sourceSchema = z.object({
  type: z.enum(['book', 'paper', 'manuscript', 'inscription', 'oral_record', 'news', 'archive']),
  title: z.string(),
  author: z.string().optional(),
  year: z.union([z.number(), z.string()]).optional(),
  language: z.string().optional(),
  location: z.string().optional(),
  url: z.string().url().optional(),
  access: z.enum(['open', 'paywall', 'offline']).optional(),
  retrieved_at: z.string().optional(),
  note: z.string().optional(),
});

const entrySchema = z.object({
  id: z.string(),
  name_primary: z.string(),
  name_original: z.string(),
  name_aliases: z.array(z.string()).optional(),
  name_translations: z.record(z.string()).optional(),
  hero_image: z.string().optional(),
  hero_image_alt: z.string().optional(),
  hero_image_credit: z.string().optional(),
  culture_path: z.string(),
  entity_type: z.enum(['deity', 'creature', 'spirit', 'event', 'place', 'ritual', 'motif']),
  era: z.string().optional(),
  geo_region: z.string().optional(),
  geo_coords: z.tuple([z.number(), z.number()]).optional(),
  summary: z.string().max(280),
  attributes: z.array(z.string()).optional(),
  related_entries: z.array(z.string()).optional(),
  parallel_motifs: z.array(z.object({entry_id: z.string(), relation: z.string()})).optional(),
  primary_sources: z.array(sourceSchema).min(1),
  secondary_sources: z.array(sourceSchema).optional(),
  confidence: z.enum(['attested', 'documented', 'folk', 'speculative']),
  first_recorded: z.string().optional(),
  created_at: z.string(),
  updated_at: z.string(),
  curator: z.string(),
  review_status: z.enum(['draft', 'in_review', 'published', 'archived']),
  llm_assisted: z.boolean(),
});

const base = 'C:/Users/Hector/Documents/lingxi-claw/20260704-13-50-36-390/mythos-atlas/mvp-site/src/content/entries';
const files = ['sanhun-qipo-daoist', 'fengshui-daoist', 'neidan-daoist', 'fengdu-daoist', 'tiangong-daoist'];
for (const f of files) {
  const content = fs.readFileSync(base + '/' + f + '.md', 'utf-8');
  const parsed = matter(content);
  const result = entrySchema.safeParse(parsed.data);
  if (result.success) {
    console.log(f + ': PASS');
  } else {
    console.log(f + ': FAIL');
    for (const issue of result.error.issues) {
      console.log('  -> ' + issue.path.join('.') + ': ' + issue.message);
    }
  }
}
