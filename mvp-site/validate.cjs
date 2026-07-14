// Mythos Atlas 质量门禁
// 用法: node validate.cjs
// 检查: (1) summary长度  (2) hero_image对应文件存在  (3) YAML title冒号  (4) 必填字段
// 独立于Astro schema,更严格的报告

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const ENTRIES = path.join(__dirname, 'src/content/entries');
const IMAGES = path.join(__dirname, 'public/images/entries');

const files = fs.readdirSync(ENTRIES).filter(f => f.endsWith('.md'));

const errors = [];
const warnings = [];
const stats = {
  total: files.length,
  missing_hero: 0,
  summary_over_280: 0,
  summary_over_320: 0,
  missing_required: 0,
  duplicate_id: 0,
};

const requiredFields = ['id', 'name_primary', 'culture_path', 'entity_type', 'summary', 'primary_sources', 'confidence', 'created_at', 'updated_at', 'curator', 'review_status'];
const seenIds = new Map();

for (const f of files) {
  const filepath = path.join(ENTRIES, f);
  const content = fs.readFileSync(filepath, 'utf-8');

  let parsed;
  try {
    parsed = matter(content);
  } catch (e) {
    errors.push(`${f}: YAML parse error - ${e.message}`);
    continue;
  }
  const d = parsed.data;

  // 必填字段
  for (const rf of requiredFields) {
    if (d[rf] === undefined) {
      errors.push(`${f}: missing required field '${rf}'`);
      stats.missing_required++;
    }
  }

  // ID重复
  if (d.id) {
    if (seenIds.has(d.id)) {
      errors.push(`${f}: duplicate id '${d.id}' (also in ${seenIds.get(d.id)})`);
      stats.duplicate_id++;
    } else {
      seenIds.set(d.id, f);
    }
    // ID与文件名对应
    const expectedId = f.replace(/\.md$/, '');
    if (d.id !== expectedId) {
      warnings.push(`${f}: id '${d.id}' does not match filename '${expectedId}'`);
    }
  }

  // summary长度
  if (d.summary) {
    if (d.summary.length > 320) {
      errors.push(`${f}: summary too long (${d.summary.length} > 320)`);
      stats.summary_over_320++;
    } else if (d.summary.length > 280) {
      warnings.push(`${f}: summary long (${d.summary.length} > 280)`);
      stats.summary_over_280++;
    }
  }

  // hero_image存在性
  if (d.hero_image) {
    const heroName = d.hero_image.replace(/^\//, '').replace('images/entries/', '').replace('mythos-atlas/', '');
    const heroFile = path.basename(heroName);
    const heroPath = path.join(IMAGES, heroFile);
    if (!fs.existsSync(heroPath)) {
      warnings.push(`${f}: hero_image file missing: ${heroFile}`);
      stats.missing_hero++;
    }
  } else {
    // 无hero_image字段
    const expectedHero = path.join(IMAGES, f.replace(/\.md$/, '.jpg'));
    if (fs.existsSync(expectedHero)) {
      warnings.push(`${f}: no hero_image field but ${f.replace(/\.md$/, '.jpg')} exists`);
    } else {
      stats.missing_hero++;
    }
  }

  // primary_sources校验
  if (d.primary_sources && Array.isArray(d.primary_sources)) {
    if (d.primary_sources.length < 1) {
      errors.push(`${f}: primary_sources empty`);
    }
    d.primary_sources.forEach((src, i) => {
      if (!src.title) errors.push(`${f}: primary_sources[${i}] missing title`);
      if (!src.type) errors.push(`${f}: primary_sources[${i}] missing type`);
    });
  }
}

// 输出
console.log('='.repeat(60));
console.log('Mythos Atlas Quality Report');
console.log('='.repeat(60));
console.log(`Total entries:        ${stats.total}`);
console.log(`Missing hero image:   ${stats.missing_hero}`);
console.log(`Summary > 280 chars:  ${stats.summary_over_280}`);
console.log(`Summary > 320 chars:  ${stats.summary_over_320}`);
console.log(`Missing required:     ${stats.missing_required}`);
console.log(`Duplicate IDs:        ${stats.duplicate_id}`);
console.log();
console.log(`Errors:   ${errors.length}`);
console.log(`Warnings: ${warnings.length}`);
console.log();

if (errors.length > 0) {
  console.log('--- ERRORS ---');
  errors.slice(0, 30).forEach(e => console.log('  ' + e));
  if (errors.length > 30) console.log(`  ... and ${errors.length - 30} more`);
  console.log();
}

if (warnings.length > 0 && process.argv.includes('--verbose')) {
  console.log('--- WARNINGS ---');
  warnings.slice(0, 50).forEach(w => console.log('  ' + w));
  if (warnings.length > 50) console.log(`  ... and ${warnings.length - 50} more`);
}

process.exit(errors.length > 0 ? 1 : 0);
