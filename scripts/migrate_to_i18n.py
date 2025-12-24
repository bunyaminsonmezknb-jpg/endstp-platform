#!/usr/bin/env python3
"""
PHASE 2 I18N Migration Scanner - Enhanced Version

Scans compliance headers AND TODO tags for comprehensive migration planning.
Provides detailed checklist for Phase 2 implementation.

Usage:
    python scripts/migrate_to_i18n.py
    python scripts/migrate_to_i18n.py --export docs/PHASE2_MIGRATION_PLAN.md
    python scripts/migrate_to_i18n.py --summary  # Quick overview
"""

import os
import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timezone
from pathlib import Path

class ComplianceHeaderParser:
    """Parse GLOBAL-FIRST compliance headers from Python files"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.has_header = False
        self.localization_status = {}
        self.hardcoded_items = []
        self.migration_notes = []
        self.file_created = None
        self.file_phase = None
    
    def parse(self) -> bool:
        """Parse compliance header, return True if found"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return False
        
        if "GLOBAL-FIRST COMPLIANCE HEADER" not in content:
            return False
        
        self.has_header = True
        
        # Extract header section
        try:
            header_match = re.search(
                r'# =+\s*\n# GLOBAL-FIRST COMPLIANCE HEADER.*?# =+',
                content,
                re.DOTALL
            )
            if not header_match:
                return True
            
            header_text = header_match.group(0)
            
            # Parse created date
            created_match = re.search(r'Created:\s*(\d{4}-\d{2}-\d{2})', header_text)
            if created_match:
                self.file_created = created_match.group(1)
            
            # Parse phase
            phase_match = re.search(r'Phase:\s*([^\n]+)', header_text)
            if phase_match:
                self.file_phase = phase_match.group(1).strip()
            
            # Parse localization status
            self._parse_localization_status(header_text)
            
            # Parse hardcoded items
            self._parse_hardcoded_items(header_text)
            
            # Parse migration notes
            self._parse_migration_notes(header_text)
            
        except Exception as e:
            print(f"Warning: Error parsing header in {self.filepath}: {e}")
        
        return True
    
    def _parse_localization_status(self, header_text: str):
        """Extract localization status checkboxes"""
        status_match = re.search(
            r'LOCALIZATION STATUS:(.*?)(?=\n#\s*📋|$)',
            header_text,
            re.DOTALL
        )
        if not status_match:
            return
        
        status_section = status_match.group(1)
        
        self.localization_status = {
            'utc_datetime': '[X]' in status_section.split('\n')[1] if len(status_section.split('\n')) > 1 else False,
            'multi_language': '[X]' in status_section.split('\n')[2] if len(status_section.split('\n')) > 2 else False,
            'db_columns': '[X]' in status_section.split('\n')[3] if len(status_section.split('\n')) > 3 else False,
            'api_language': '[X]' in status_section.split('\n')[4] if len(status_section.split('\n')) > 4 else False,
            'no_hardcoded': '[X]' in status_section.split('\n')[5] if len(status_section.split('\n')) > 5 else False,
        }
    
    def _parse_hardcoded_items(self, header_text: str):
        """Extract hardcoded items list"""
        items_match = re.search(
            r'HARDCODED ITEMS.*?:(.*?)(?=\n#\s*🚀|$)',
            header_text,
            re.DOTALL
        )
        if not items_match:
            return
        
        items_section = items_match.group(1)
        for line in items_section.split('\n'):
            line = line.strip('#').strip()
            if line.startswith('-') and '→' in line:
                self.hardcoded_items.append(line.lstrip('- '))
    
    def _parse_migration_notes(self, header_text: str):
        """Extract migration notes"""
        notes_match = re.search(
            r'MIGRATION NOTES.*?:(.*?)(?=\n#\s*📚|$)',
            header_text,
            re.DOTALL
        )
        if not notes_match:
            return
        
        notes_section = notes_match.group(1)
        for line in notes_section.split('\n'):
            line = line.strip('#').strip()
            if line.startswith('-') and line != '- (Actions will be listed here)':
                self.migration_notes.append(line.lstrip('- '))

class EnhancedMigrationScanner:
    """Enhanced scanner combining headers and TODO tags"""
    
    def __init__(self, root_dir: str = "backend"):
        self.root_dir = root_dir
        self.results = []
    
    def scan(self) -> List[Dict]:
        """Scan all Python files for migration items"""
        for root, dirs, files in os.walk(self.root_dir):
            # Skip cache and venv
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.venv', 'venv', '.pytest_cache']]
            
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    filepath = os.path.join(root, file)
                    self._scan_file(filepath)
        
        return self.results
    
    def _scan_file(self, filepath: str):
        """Scan single file for compliance and migration items"""
        # Parse header
        header_parser = ComplianceHeaderParser(filepath)
        header_parser.parse()
        
        # Find TODO tags
        todo_tags = self._find_todo_tags(filepath)
        
        # Only include files that need migration
        if header_parser.has_header or todo_tags:
            self.results.append({
                'file': filepath,
                'has_header': header_parser.has_header,
                'created': header_parser.file_created,
                'phase': header_parser.file_phase,
                'localization_status': header_parser.localization_status,
                'hardcoded_items': header_parser.hardcoded_items,
                'migration_notes': header_parser.migration_notes,
                'todo_tags': todo_tags,
                'needs_migration': len(header_parser.hardcoded_items) > 0 or len(todo_tags) > 0
            })
    
    def _find_todo_tags(self, filepath: str) -> List[Tuple[int, str]]:
        """Find all TODO: PHASE-2-I18N tags with line numbers"""
        tags = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if 'TODO: PHASE-2-I18N' in line:
                        tags.append((i, line.strip()))
        except:
            pass
        return tags
    
    def generate_summary(self) -> str:
        """Generate quick summary"""
        total_files = len(self.results)
        with_headers = sum(1 for r in self.results if r['has_header'])
        with_todos = sum(1 for r in self.results if r['todo_tags'])
        needs_migration = sum(1 for r in self.results if r['needs_migration'])
        total_items = sum(len(r['hardcoded_items']) + len(r['todo_tags']) for r in self.results)
        
        summary = f"""
🌍 PHASE 2 MIGRATION SUMMARY
{'=' * 50}
Files scanned: {total_files}
  - With compliance headers: {with_headers}
  - With TODO tags: {with_todos}
  - Needing migration: {needs_migration}

Total migration items: {total_items}

Status:
  ✅ Ready for Phase 2: {with_headers} files have headers
  ⚠️  Need headers: {total_files - with_headers} files

Run with --export to see full details.
"""
        return summary
    
    def generate_report(self) -> str:
        """Generate comprehensive migration report"""
        report = []
        report.append("=" * 70)
        report.append("PHASE 2 I18N MIGRATION REPORT (Enhanced)")
        report.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append("=" * 70)
        report.append("")
        
        # Statistics
        total_files = len(self.results)
        with_headers = sum(1 for r in self.results if r['has_header'])
        needs_migration = sum(1 for r in self.results if r['needs_migration'])
        total_hardcoded = sum(len(r['hardcoded_items']) for r in self.results)
        total_todos = sum(len(r['todo_tags']) for r in self.results)
        
        report.append("�� STATISTICS")
        report.append("-" * 70)
        report.append(f"Total files analyzed: {total_files}")
        report.append(f"Files with compliance headers: {with_headers} ({with_headers/total_files*100:.0f}%)")
        report.append(f"Files needing migration: {needs_migration}")
        report.append(f"Total hardcoded items: {total_hardcoded}")
        report.append(f"Total TODO tags: {total_todos}")
        report.append("")
        
        # File details
        report.append("📋 FILES REQUIRING MIGRATION")
        report.append("-" * 70)
        
        for idx, result in enumerate(self.results, 1):
            if not result['needs_migration']:
                continue
            
            report.append(f"\n{idx}. {result['file']}")
            
            if result['has_header']:
                report.append("   ✅ Has compliance header")
                if result['created']:
                    report.append(f"      Created: {result['created']}")
                if result['phase']:
                    report.append(f"      Phase: {result['phase']}")
                
                # Localization status
                status = result['localization_status']
                if status:
                    complete = sum(1 for v in status.values() if v)
                    total = len(status)
                    report.append(f"      Progress: {complete}/{total} items complete")
                    
                    incomplete = [k.replace('_', ' ').title() for k, v in status.items() if not v]
                    if incomplete:
                        report.append(f"      ⚠️  Incomplete: {', '.join(incomplete)}")
                
                # Hardcoded items
                if result['hardcoded_items']:
                    report.append(f"   📝 Hardcoded items ({len(result['hardcoded_items'])}):")
                    for item in result['hardcoded_items']:
                        report.append(f"      - {item}")
                
                # Migration notes
                if result['migration_notes']:
                    report.append(f"   🚀 Migration notes:")
                    for note in result['migration_notes']:
                        report.append(f"      - {note}")
            else:
                report.append("   ❌ Missing compliance header - ADD FIRST!")
            
            # TODO tags
            if result['todo_tags']:
                report.append(f"   🏷️  TODO tags ({len(result['todo_tags'])}):")
                for line_num, tag in result['todo_tags'][:3]:  # Show max 3
                    report.append(f"      Line {line_num}: {tag[:60]}...")
                if len(result['todo_tags']) > 3:
                    report.append(f"      ... and {len(result['todo_tags']) - 3} more")
        
        # Migration checklist
        report.append("")
        report.append("=" * 70)
        report.append("✅ PHASE 2 MIGRATION CHECKLIST")
        report.append("=" * 70)
        report.append("")
        report.append("PREPARATION:")
        report.append("  [ ] Review this migration report")
        report.append(f"  [ ] Add headers to {total_files - with_headers} files without them")
        report.append("  [ ] Update existing headers with current items")
        report.append("  [ ] Create Phase 2 branch: git checkout -b phase-2-i18n")
        report.append("")
        report.append("DATABASE (Week 1):")
        report.append("  [ ] Create migration: 010_i18n_system.sql")
        report.append("  [ ] Add languages table (tr, en, ko, ja, ar, es, fr, de)")
        report.append("  [ ] Add translations table")
        report.append("  [ ] Seed Turkish translations")
        report.append("  [ ] Seed English translations")
        report.append("")
        report.append("BACKEND HELPERS (Week 1):")
        report.append("  [ ] Create helpers/i18n.py")
        report.append("  [ ] Implement get_user_language()")
        report.append("  [ ] Implement get_translation()")
        report.append("  [ ] Implement format_date_localized()")
        report.append("  [ ] Add language detection middleware")
        report.append("")
        report.append(f"BACKEND FILES ({needs_migration} files - Week 2):")
        report.append("  [ ] Update function signatures (add language param)")
        report.append("  [ ] Replace TURKISH_MONTHS with database lookups")
        report.append("  [ ] Replace format_date_turkish() calls")
        report.append("  [ ] Update API endpoints (Accept-Language)")
        report.append("  [ ] Add language parameter to responses")
        report.append("")
        report.append("FRONTEND (Week 2-3):")
        report.append("  [ ] Install: npm install next-intl")
        report.append("  [ ] Create locales/tr/ and locales/en/")
        report.append("  [ ] Create translation JSON files")
        report.append("  [ ] Implement LanguageProvider")
        report.append("  [ ] Create LanguageSwitcher component")
        report.append("  [ ] Replace hardcoded text with t() calls")
        report.append("  [ ] Test language switching")
        report.append("")
        report.append("TESTING (Week 3):")
        report.append("  [ ] Unit tests for translation helpers")
        report.append("  [ ] API tests with Accept-Language header")
        report.append("  [ ] Frontend tests for language switching")
        report.append("  [ ] Visual regression tests")
        report.append("  [ ] Performance benchmarks")
        report.append("")
        report.append("DEPLOYMENT (Week 4):")
        report.append("  [ ] Staging deployment")
        report.append("  [ ] UAT with Turkish/English users")
        report.append("  [ ] Production deployment")
        report.append("  [ ] Monitor translation performance")
        report.append("  [ ] Update documentation")
        report.append("")
        
        return '\n'.join(report)

def main():
    import sys
    
    scanner = EnhancedMigrationScanner()
    results = scanner.scan()
    
    # Check mode
    if '--summary' in sys.argv:
        print(scanner.generate_summary())
        return
    
    # Generate full report
    report = scanner.generate_report()
    print(report)
    
    # Export if requested
    if '--export' in sys.argv:
        try:
            export_idx = sys.argv.index('--export')
            output_file = sys.argv[export_idx + 1] if len(sys.argv) > export_idx + 1 else 'docs/PHASE2_MIGRATION_PLAN.md'
        except (ValueError, IndexError):
            output_file = 'docs/PHASE2_MIGRATION_PLAN.md'
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Report exported to: {output_file}")

if __name__ == '__main__':
    main()
