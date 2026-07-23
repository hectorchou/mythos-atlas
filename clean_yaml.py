import os
import re

# 项目路径
base_dir = r"C:\Users\Hector\Documents\lingxi-claw\20260704-13-50-36-390\mythos-atlas\mvp-site\src\content\entries"
files = [
    "sekhmet-egypt.md",
    "bastet-egypt.md",
    "nut-egypt.md",
    "geb-egypt.md",
    "khonsu-egypt.md"
]

for filename in files:
    path = os.path.join(base_dir, filename)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    
    # 提取 frontmatter
    match = re.match(r"^(---\n.*?\n---\n)(.*)", content, re.DOTALL)
    if not match:
        print(f"{filename}: 未找到 frontmatter")
        continue
        
    fm, body = match.groups()
    
    # 检查 summary 长度
    summary_match = re.search(r"summary:\s*(.*)\n", fm)
    if summary_match:
        summary_text = summary_match.group(1).strip('"')
        length = len(summary_text)
        print(f"{filename}: summary 长度 {length} 字符")
        if length > 230:
            print(f"  警告: 超过 230 字符")
    
    # 清理 flow 列表中的引号和等号
    def fix_list(match):
        text = match.group(0)
        # 移除所有英文双引号，替换等号为"为"
        text = text.replace('"', '').replace('=', '为')
        return text
    
    new_fm = re.sub(r'\[[^\]]*\]', fix_list, fm)
    
    # 修复日期字符串引号
    new_fm = re.sub(r'(created_at|updated_at): (\d{4}-\d{2}-\d{2})', r'\1: "\2"', new_fm)
    
    if new_fm != fm:
        print(f"{filename}: 清理完成")
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_fm + body)
    else:
        print(f"{filename}: 无需修改")
