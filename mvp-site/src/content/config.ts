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

const timelineEntrySchema = z.object({
  period: z.string().optional(),
  event: z.string().optional(),
});

const crossCultureSchema = z.object({
  culture: z.string(),
  entity: z.string(),
  relation: z.string(),
});

const parallelMotifSchema = z.object({
  entry_id: z.string(),
  relation: z.string(),
});

const entries = defineCollection({
  type: 'content',
  schema: z.object({
    // 核心身份
    id: z.string(),
    name_primary: z.string(),
    name_original: z.string(),
    name_aliases: z.array(z.string()).optional(),
    name_translations: z.record(z.string()).optional(),

    // 视觉
    hero_image: z.string().optional(),
    hero_image_alt: z.string().optional(),
    hero_image_credit: z.string().optional(),

    // 定位
    culture_path: z.string(),
    entity_type: z.enum(['deity', 'creature', 'spirit', 'event', 'place', 'ritual', 'motif']),
    era: z.string().optional(),
    geo_region: z.string().optional(),
    geo_coords: z.tuple([z.number(), z.number()]).optional(),

    // 内容
    summary: z.string().max(320),
    attributes: z.array(z.any()).optional(),

    // 关系网络（合并模板A/B）
    related_entries: z.array(z.string()).optional(),
    parallel_motifs: z.array(parallelMotifSchema).optional(),
    parallels: z.array(z.any()).optional(),
    cross_culture_parallels: z.array(crossCultureSchema).optional(),
    parents: z.array(z.any()).optional(),
    children: z.array(z.any()).optional(),
    consort: z.array(z.any()).optional(),
    siblings: z.array(z.any()).optional(),
    associates: z.array(z.any()).optional(),

    // 属性扩展（模板B）
    epithets: z.array(z.any()).optional(),
    variants: z.array(z.any()).optional(),
    cult_center: z.array(z.any()).optional(),
    domain: z.union([z.string(), z.array(z.string())]).optional(),
    domains: z.array(z.string()).optional(),
    weapon: z.union([z.string(), z.array(z.string())]).optional(),
    mount: z.string().optional(),
    sacred_animal: z.union([z.string(), z.array(z.string())]).optional(),
    manifestations: z.array(z.any()).optional(),
    key_concepts: z.array(z.string()).optional(),
    key_texts: z.array(z.string()).optional(),
    key_figures: z.array(z.string()).optional(),
    key_deities: z.array(z.string()).optional(),
    key_narratives: z.array(z.string()).optional(),
    key_narratives: z.array(z.string()).optional(),
    core_concepts: z.array(z.string()).optional(),
    core_deities: z.array(z.string()).optional(),
    related_concepts: z.array(z.string()).optional(),
    cosmological_layers: z.array(z.string()).optional(),
    ritual_practices: z.array(z.string()).optional(),
    cult_practices: z.array(z.string()).optional(),
    cult_symbols: z.array(z.string()).optional(),
    subcategories: z.array(z.string()).optional(),
    pantheon: z.array(z.string()).optional(),

    // 时间线与叙事结构
    timeline: z.array(timelineEntrySchema).optional(),
    evolution_timeline: z.array(timelineEntrySchema).optional(),
    flow: z.array(z.any()).optional(),
    tags: z.array(z.any()).optional(),

    // 学术分析
    academic_insight: z.string().optional(),

    // 来源与校验
    primary_sources: z.array(sourceSchema).min(1),
    secondary_sources: z.array(sourceSchema).optional(),
    confidence: z.enum(['attested', 'documented', 'folk', 'speculative']),
    first_recorded: z.string().optional(),
    first_attested_year: z.union([z.number(), z.string()]).optional(),
    last_edited_year: z.union([z.number(), z.string()]).optional(),

    // 元数据
    created_at: z.string(),
    updated_at: z.string(),
    curator: z.string(),
    review_status: z.enum(['draft', 'in_review', 'published', 'archived']),
    llm_assisted: z.boolean(),

    // 长尾字段（模板B少量使用，放最后）
    structured_data: z.any().optional(),
    parents_note: z.string().optional(),
    triad: z.array(z.string()).optional(),
    afterlife_triad: z.array(z.string()).optional(),
    six_amesha_spentas: z.array(z.string()).optional(),
    seven_creations: z.array(z.string()).optional(),
    three_forms: z.array(z.string()).optional(),
    three_fires: z.array(z.string()).optional(),
    associated_star: z.string().optional(),
    avestan_form: z.string().optional(),
    middle_persian: z.string().optional(),
    new_persian: z.string().optional(),
    pahlavi: z.string().optional(),
    vedic_counterpart: z.string().optional(),
    syncretism: z.array(z.string()).optional(),
    adversary: z.union([z.string(), z.array(z.string())]).optional(),
    origin: z.string().optional(),
    destiny: z.string().optional(),
    main_daevas: z.array(z.string()).optional(),
    attacks: z.array(z.string()).optional(),
    outcome: z.string().optional(),
    participants: z.array(z.string()).optional(),
    passage: z.string().optional(),
    style: z.string().optional(),
    method: z.string().optional(),
    dates: z.union([z.string(), z.array(z.string())]).optional(),
    mechanism: z.string().optional(),
    paired_with: z.union([z.string(), z.array(z.string())]).optional(),
    god_name: z.string().optional(),
    humans: z.string().optional(),
    standard: z.string().optional(),
    center: z.union([z.string(), z.array(z.string())]).optional(),
    creator: z.union([z.string(), z.array(z.string())]).optional(),
    temple: z.union([z.string(), z.array(z.string())]).optional(),
    location: z.union([z.string(), z.array(z.string())]).optional(),
    version: z.union([z.string(), z.array(z.string())]).optional(),
    period: z.union([z.string(), z.array(z.string())]).optional(),
    event: z.union([z.string(), z.array(z.string())]).optional(),
    detail: z.union([z.string(), z.array(z.string())]).optional(),
    description: z.union([z.string(), z.array(z.string())]).optional(),
    source_ref: z.union([z.string(), z.array(z.string())]).optional(),
  }),
});

export const collections = { entries };
