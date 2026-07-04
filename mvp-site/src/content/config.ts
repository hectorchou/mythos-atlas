import { defineCollection, z } from 'astro:content';

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

const entries = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    name_primary: z.string(),
    name_original: z.string(),
    name_aliases: z.array(z.string()).optional(),
    name_translations: z.record(z.string()).optional(),

    culture_path: z.string(),
    entity_type: z.enum(['deity', 'creature', 'spirit', 'event', 'place', 'ritual', 'motif']),
    era: z.string().optional(),
    geo_region: z.string().optional(),
    geo_coords: z.tuple([z.number(), z.number()]).optional(),

    summary: z.string().max(280),
    attributes: z.array(z.string()).optional(),
    related_entries: z.array(z.string()).optional(),
    parallel_motifs: z.array(z.object({
      entry_id: z.string(),
      relation: z.string(),
    })).optional(),

    primary_sources: z.array(sourceSchema).min(1),
    secondary_sources: z.array(sourceSchema).optional(),
    confidence: z.enum(['attested', 'documented', 'folk', 'speculative']),
    first_recorded: z.string().optional(),

    created_at: z.string(),
    updated_at: z.string(),
    curator: z.string(),
    review_status: z.enum(['draft', 'in_review', 'published', 'archived']),
    llm_assisted: z.boolean(),
  }),
});

export const collections = { entries };
