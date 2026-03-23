#!/usr/bin/env python3
"""
Thesis Repository Structure Builder
Builds the required directory structure and copies files with proper organization.
"""

import os
import sys
from pathlib import Path
from shutil import copy2, copytree, rmtree
import json

# Define paths
work_dir = Path(r'C:\Users\oussa\Desktop\Study\Thes\2026\Thesis Workplace\Wokspace\thesis')
github_ws = work_dir / 'github_thesis_workspace'
thesis_pkg = work_dir / 'THESIS_PACKAGE'
target = github_ws / 'thesis-github-package'

print('='*70)
print('THESIS REPOSITORY STRUCTURE BUILDER')
print('='*70)
print(f'Working Directory: {github_ws}')
print(f'Target: {target}')
print(f'Source 1: {thesis_pkg}')
print(f'Source 2: {github_ws}')
print()

# ============================================================================
# STEP 1: INSPECT SOURCES
# ============================================================================
print('STEP 1: INSPECTING SOURCES')
print('-'*70)

print(f'\n[INFO] Target exists: {target.exists()}')
print(f'[INFO] Source THESIS_PACKAGE exists: {thesis_pkg.exists()}')
print(f'[INFO] Source github_thesis_workspace exists: {github_ws.exists()}')

if thesis_pkg.exists():
    pkg_contents = list(thesis_pkg.iterdir())
    print(f'[INFO] THESIS_PACKAGE contents ({len(pkg_contents)} items):')
    for item in pkg_contents[:10]:
        print(f'       - {item.name}')
        
if github_ws.exists():
    ws_contents = list(github_ws.iterdir())
    print(f'[INFO] github_thesis_workspace contents ({len(ws_contents)} items):')
    for item in ws_contents[:10]:
        if item.name not in ['thesis-github-package', 'build_thesis_structure.py']:
            print(f'       - {item.name}')

# ============================================================================
# STEP 2: CREATE REQUIRED DIRECTORY STRUCTURE
# ============================================================================
print('\n' + '='*70)
print('STEP 2: CREATING DIRECTORY STRUCTURE')
print('-'*70)

required_dirs = [
    '01_data_collection',
    '02_benchmarks',
    '03_scripts/execution',
    '03_scripts/analysis',
    '03_scripts/prof_bootstrap',
    '03_scripts/system_optimization',
    '04_results/figures',
    '04_results/analysis_exports',
    '04_results/raw_json',
    '05_reproducibility',
]

created_count = 0
for dir_name in required_dirs:
    dir_path = target / dir_name
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f'[CREATED] {dir_path.name}')
        created_count += 1
    else:
        print(f'[EXISTS] {dir_path.name}')

print(f'\n[SUMMARY] Created/Verified {created_count} directories')

# ============================================================================
# STEP 3: COPY FILES ACCORDING TO MAPPING
# ============================================================================
print('\n' + '='*70)
print('STEP 3: COPYING FILES (Non-JSON)')
print('-'*70)

copy_operations = []
total_copied = 0
source_summaries = {}

# Mapping 1: benchmarks
src_benchmarks = github_ws / 'benchmarks'
if src_benchmarks.exists():
    count = 0
    for item in src_benchmarks.rglob('*'):
        if item.is_file() and not item.suffix == '.json':
            rel_path = item.relative_to(src_benchmarks)
            dest = target / '02_benchmarks' / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            copy2(item, dest)
            count += 1
            total_copied += 1
    source_summaries['benchmarks'] = count
    print(f'[COPIED] benchmarks -> 02_benchmarks ({count} files)')
else:
    print(f'[SKIP] benchmarks (source not found)')
    source_summaries['benchmarks'] = 0

# Mapping 2: scripts from github_thesis_workspace
src_scripts = github_ws / 'scripts'
if src_scripts.exists():
    count = 0
    for item in src_scripts.rglob('*'):
        if item.is_file() and not item.suffix == '.json':
            rel_path = item.relative_to(src_scripts)
            # Map to appropriate subfolder
            if 'prof' in item.name.lower() or 'bootstrap' in item.name.lower():
                dest = target / '03_scripts/prof_bootstrap' / rel_path
            elif 'optim' in item.name.lower() or 'system' in item.name.lower():
                dest = target / '03_scripts/system_optimization' / rel_path
            elif 'exec' in item.name.lower() or 'run' in item.name.lower():
                dest = target / '03_scripts/execution' / rel_path
            else:
                dest = target / '03_scripts/analysis' / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            copy2(item, dest)
            count += 1
            total_copied += 1
    source_summaries['github_scripts'] = count
    print(f'[COPIED] scripts -> 03_scripts/* ({count} files)')
else:
    print(f'[SKIP] scripts (source not found)')
    source_summaries['github_scripts'] = 0

# Mapping 3: visualizations
src_viz = github_ws / 'visualizations'
if src_viz.exists():
    count = 0
    for item in src_viz.rglob('*'):
        if item.is_file() and not item.suffix == '.json':
            rel_path = item.relative_to(src_viz)
            dest = target / '04_results/figures' / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            copy2(item, dest)
            count += 1
            total_copied += 1
    source_summaries['visualizations'] = count
    print(f'[COPIED] visualizations -> 04_results/figures ({count} files)')
else:
    print(f'[SKIP] visualizations (source not found)')
    source_summaries['visualizations'] = 0

# Mapping 4: THESIS_PACKAGE - Prof_script
src_prof = thesis_pkg / 'Prof_script'
if src_prof.exists():
    count = 0
    for item in src_prof.rglob('*'):
        if item.is_file() and not item.suffix == '.json':
            rel_path = item.relative_to(src_prof)
            dest = target / '03_scripts/prof_bootstrap' / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            copy2(item, dest)
            count += 1
            total_copied += 1
    source_summaries['Prof_script'] = count
    print(f'[COPIED] Prof_script -> 03_scripts/prof_bootstrap ({count} files)')
else:
    print(f'[SKIP] Prof_script (source not found)')
    source_summaries['Prof_script'] = 0

# Mapping 5: THESIS_PACKAGE - system_optimization
src_sysopt = thesis_pkg / 'system_optimization'
if src_sysopt.exists():
    count = 0
    for item in src_sysopt.rglob('*'):
        if item.is_file() and not item.suffix == '.json':
            rel_path = item.relative_to(src_sysopt)
            dest = target / '03_scripts/system_optimization' / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            copy2(item, dest)
            count += 1
            total_copied += 1
    source_summaries['system_optimization'] = count
    print(f'[COPIED] system_optimization -> 03_scripts/system_optimization ({count} files)')
else:
    print(f'[SKIP] system_optimization (source not found)')
    source_summaries['system_optimization'] = 0

# Mapping 6: THESIS_PACKAGE - Top-level run/inject scripts
src_pkg_top = thesis_pkg
exec_count = 0
for item in src_pkg_top.glob('*.py'):
    if ('run' in item.name.lower() or 'inject' in item.name.lower()) and not item.suffix == '.json':
        dest = target / '03_scripts/execution' / item.name
        copy2(item, dest)
        exec_count += 1
        total_copied += 1
source_summaries['THESIS_toplevel_scripts'] = exec_count
if exec_count > 0:
    print(f'[COPIED] THESIS_PACKAGE top-level scripts -> 03_scripts/execution ({exec_count})')
else:
    print(f'[SKIP] THESIS_PACKAGE top-level scripts (none found)')

# Mapping 7: THESIS_PACKAGE - finals .txt outputs
finals_count = 0
for item in src_pkg_top.glob('finals*'):
    if item.is_file() and item.suffix == '.txt':
        dest = target / '04_results/analysis_exports' / item.name
        copy2(item, dest)
        finals_count += 1
        total_copied += 1
source_summaries['finals_txt'] = finals_count
if finals_count > 0:
    print(f'[COPIED] THESIS_PACKAGE finals .txt -> 04_results/analysis_exports ({finals_count})')
else:
    print(f'[SKIP] THESIS_PACKAGE finals .txt (none found)')

# Mapping 8: THESIS_PACKAGE - documentation
src_docs = thesis_pkg / 'benchmark_documentation'
if src_docs.exists():
    docs_count = 0
    for item in src_docs.rglob('*'):
        if item.is_file() and not item.suffix == '.json':
            rel_path = item.relative_to(src_docs)
            dest = target / '01_data_collection' / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            copy2(item, dest)
            docs_count += 1
            total_copied += 1
    source_summaries['benchmark_documentation'] = docs_count
    print(f'[COPIED] benchmark_documentation -> 01_data_collection ({docs_count})')
else:
    print(f'[SKIP] benchmark_documentation (source not found)')
    source_summaries['benchmark_documentation'] = 0

# Mapping 9: THESIS_PACKAGE - BENCHMARK_SUMMARY.md and PROJECT_STATUS.md
md_count = 0
for fname in ['BENCHMARK_SUMMARY.md', 'PROJECT_STATUS.md']:
    src_file = thesis_pkg / fname
    if src_file.exists():
        dest_file = target / '01_data_collection' / fname
        copy2(src_file, dest_file)
        md_count += 1
        total_copied += 1
        print(f'[COPIED] {fname} -> 01_data_collection')
source_summaries['status_docs'] = md_count

print(f'\n[SUMMARY] Total files copied: {total_copied}')

# ============================================================================
# STEP 4: REMOVE ALL .JSON FILES FROM TARGET
# ============================================================================
print('\n' + '='*70)
print('STEP 4: REMOVING .JSON FILES FROM TARGET')
print('-'*70)

json_count = 0
json_removed = []
for json_file in target.rglob('*.json'):
    try:
        json_file.unlink()
        json_removed.append(json_file.relative_to(target))
        json_count += 1
    except Exception as e:
        print(f'[ERROR] Failed to remove {json_file}: {e}')

if json_removed:
    print(f'[REMOVED] {json_count} JSON files:')
    for jf in json_removed[:10]:
        print(f'    - {jf}')
    if len(json_removed) > 10:
        print(f'    ... and {len(json_removed) - 10} more')
else:
    print(f'[INFO] No JSON files to remove')

print(f'[SUMMARY] Removed {json_count} .json files')

# ============================================================================
# STEP 5: CREATE README.MD FILES
# ============================================================================
print('\n' + '='*70)
print('STEP 5: CREATING README.MD FILES')
print('-'*70)

readmes = {
    '01_data_collection': '''# Data Collection

This directory contains benchmark documentation, data collection methodology, and foundational research artifacts for the thesis study.

## Contents
- `benchmark_documentation/`: Detailed documentation of benchmark procedures
- `BENCHMARK_SUMMARY.md`: Summary of all benchmarks conducted
- `PROJECT_STATUS.md`: Current project status and milestones

## Structure
All benchmark documentation and status reports are organized hierarchically for easy reference during reproducibility phases.
''',
    
    '02_benchmarks': '''# Benchmarks

This directory contains all benchmark suites, performance measurement scripts, and benchmark utilities.

## Contents
Includes executable benchmarks and performance profiling tools organized by category and use case.

## Usage
Execute benchmark scripts according to the methodology documented in `../01_data_collection/`.
''',
    
    '03_scripts/execution': '''# Execution Scripts

This directory contains scripts for running experiments and tests.

## Contents
- Top-level run and inject scripts for thesis experiments
- Bootstrap and initialization routines

## Usage
Execute scripts in order as specified in `../../01_data_collection/BENCHMARK_SUMMARY.md`.
''',
    
    '03_scripts/analysis': '''# Analysis Scripts

This directory contains data analysis and post-processing scripts.

## Contents
Processing and analysis routines for benchmark results.

## Usage
Run after data collection is complete to generate analysis outputs.
''',
    
    '03_scripts/prof_bootstrap': '''# Profiling and Bootstrap

This directory contains profiling utilities and bootstrap procedures.

## Contents
- Profiling tools for performance measurement
- Bootstrap initialization routines

## Usage
Deploy profiling tools before benchmark execution as documented in methodology.
''',
    
    '03_scripts/system_optimization': '''# System Optimization

This directory contains system-level optimization and configuration scripts.

## Contents
Scripts for system tuning, environment configuration, and optimization routines.

## Usage
Execute optimization scripts to prepare system for benchmark runs.
''',
    
    '03_scripts': '''# Scripts

This directory contains all executable scripts organized by functional category.

## Subdirectories
- `execution/`: Benchmark execution and test running scripts
- `analysis/`: Data analysis and post-processing routines
- `prof_bootstrap/`: Profiling and initialization utilities
- `system_optimization/`: System configuration and optimization tools

## Overview
All scripts are organized hierarchically to support reproducibility and maintenance.
''',
    
    '04_results/figures': '''# Figures

This directory contains visualizations, plots, and graphical outputs.

## Contents
- Generated figures from data analysis
- Visualization artifacts used in thesis presentation

## Format
Supports multiple formats (PNG, PDF, SVG) for publication and presentation use.
''',
    
    '04_results/analysis_exports': '''# Analysis Exports

This directory contains exported analysis results and processed outputs.

## Contents
- Text-based results and summaries
- Processed data exports
- Analysis reports

## Usage
Results are suitable for inclusion in thesis appendices and supplementary materials.
''',
    
    '04_results/raw_json': '''# Raw JSON Data

This directory is reserved for raw JSON data outputs.

## Status
Currently empty. JSON files are not archived in version control per project policy.

## Note
Direct data in this directory uses README-only strategy for version control compatibility.
''',
    
    '04_results': '''# Results

This directory contains all output artifacts and processed results.

## Subdirectories
- `figures/`: Visualizations and plots
- `analysis_exports/`: Processed analysis results and reports
- `raw_json/`: JSON data outputs (reserved)

## Overview
Organized for easy access to thesis output artifacts and supplementary materials.
''',
    
    '05_reproducibility': '''# Reproducibility

This directory contains artifacts and documentation for research reproducibility.

## Contents
- Reproduction procedures
- Environment configuration documentation
- Dependency specifications

## Purpose
Enables future reproduction of all thesis experiments and results.
''',
}

readme_count = 0
for dir_path, content in readmes.items():
    target_dir = target / dir_path
    target_dir.mkdir(parents=True, exist_ok=True)
    readme_file = target_dir / 'README.md'
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'[CREATED] {target_dir.name}/README.md')
    readme_count += 1

print(f'\n[SUMMARY] Created {readme_count} README.md files')

# ============================================================================
# STEP 6: VERIFICATION
# ============================================================================
print('\n' + '='*70)
print('STEP 6: VERIFICATION')
print('-'*70)

# Check for JSON files
json_check = list(target.rglob('*.json'))
print(f'\n[CHECK] JSON files in target: {len(json_check)}')
if json_check:
    print(f'  ✗ WARNING: Found {len(json_check)} JSON files:')
    for f in json_check[:5]:
        print(f'    - {f.relative_to(target)}')
else:
    print(f'  ✓ PASS: No .json files found')

# Check for figures
figures_dir = target / '04_results/figures'
figure_files = [f for f in figures_dir.rglob('*') if f.is_file() and f.name != 'README.md']
print(f'\n[CHECK] Figures copied: {len(figure_files)} files')
if figure_files:
    for f in figure_files[:5]:
        print(f'    - {f.relative_to(figures_dir)}')
    if len(figure_files) > 5:
        print(f'    ... and {len(figure_files) - 5} more')

# Check for scripts
scripts_root = target / '03_scripts'
script_files = [f for f in scripts_root.rglob('*') if f.is_file() and f.name != 'README.md']
print(f'\n[CHECK] Scripts copied: {len(script_files)} files')
if script_files:
    for f in script_files[:8]:
        rel = f.relative_to(scripts_root)
        print(f'    - {rel}')
    if len(script_files) > 8:
        print(f'    ... and {len(script_files) - 8} more')

# Check for benchmarks
benchmarks_dir = target / '02_benchmarks'
benchmark_files = [f for f in benchmarks_dir.rglob('*') if f.is_file() and f.name != 'README.md']
print(f'\n[CHECK] Benchmarks copied: {len(benchmark_files)} files')
if benchmark_files:
    for f in benchmark_files[:5]:
        print(f'    - {f.relative_to(benchmarks_dir)}')
    if len(benchmark_files) > 5:
        print(f'    ... and {len(benchmark_files) - 5} more')

# Check for README files
readme_files = sorted(list(target.rglob('README.md')))
print(f'\n[CHECK] README.md files present: {len(readme_files)}')
non_empty = 0
for readme in readme_files:
    size = readme.stat().st_size
    if size > 0:
        non_empty += 1
    rel_path = readme.relative_to(target)
    print(f'    - {rel_path} ({size} bytes)')

print(f'  [SUMMARY] Non-empty READMEs: {non_empty}/{len(readme_files)}')

# Verify raw_json is empty except README
raw_json_dir = target / '04_results/raw_json'
raw_json_contents = [f for f in raw_json_dir.iterdir() if f.is_file() and f.name != 'README.md']
print(f'\n[CHECK] raw_json (non-README files): {len(raw_json_contents)}')
if raw_json_contents:
    print(f'  ✗ WARNING: Found {len(raw_json_contents)} non-README files')
    for f in raw_json_contents[:5]:
        print(f'    - {f.name}')
else:
    print(f'  ✓ PASS: raw_json directory clean')

# Overall structure check
all_dirs_exist = all((target / d).exists() for d in required_dirs)
print(f'\n[CHECK] Required directory structure: {\"✓ PASS\" if all_dirs_exist else \"✗ FAIL\"}')
if all_dirs_exist:
    print(f'  All {len(required_dirs)} required directories present')

# Final summary of copy operations
print(f'\n[COPY SOURCES SUMMARY]')
for source, count in source_summaries.items():
    print(f'  {source}: {count} files')

print('\n' + '='*70)
print('EXECUTION COMPLETE')
print('='*70)
print(f'✓ Total files copied: {total_copied}')
print(f'✓ Total JSON files removed: {json_count}')
print(f'✓ Total README files created: {readme_count}')
print(f'✓ Target location: {target}')
print(f'✓ Directory structure verified')
print('='*70)
