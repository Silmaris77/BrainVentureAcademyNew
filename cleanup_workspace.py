#!/usr/bin/env python3
"""
Workspace Cleanup Script for BrainVenture Academy
Safely removes unnecessary development, test, and temporary files
"""

import os
import shutil
import datetime
from pathlib import Path

def create_backup_directory():
    """Create a backup directory with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_cleanup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir

def move_files_to_backup(files_to_remove, backup_dir):
    """Move files to backup directory instead of deleting them"""
    moved_files = []
    failed_files = []
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                # Create subdirectories in backup if needed
                relative_path = os.path.relpath(file_path)
                backup_file_path = os.path.join(backup_dir, relative_path)
                backup_file_dir = os.path.dirname(backup_file_path)
                
                os.makedirs(backup_file_dir, exist_ok=True)
                shutil.move(file_path, backup_file_path)
                moved_files.append(file_path)
            except Exception as e:
                failed_files.append((file_path, str(e)))
        else:
            print(f"⚠️  File not found: {file_path}")
    
    return moved_files, failed_files

def main():
    print("🧹 BrainVenture Academy - Workspace Cleanup")
    print("=" * 50)
    
    # Files to remove categorized
    files_to_remove = {
        "test_files": [
            "test_75_percent_requirement.py",
            "test_achievements_comprehensive.py", 
            "test_achievements_direct.py",
            "test_badge_categories.py",
            "test_badge_dashboard.py",
            "test_badge_fix.py",
            "test_badge_integration.py",
            "test_badge_system_final.py",
            "test_complete_lesson_xp.py",
            "test_course_map_final.py",
            "test_course_map_final_fixes.py",
            "test_course_map_fixes.py",
            "test_course_map_integration.py",
            "test_course_map_physics.py",
            "test_dashboard_data_access.py",
            "test_dashboard_neuroleader.py",
            "test_diagnostic_quiz.py",
            "test_final_fix.py",
            "test_final_fixes.py",
            "test_final_mind_map.py",
            "test_final_mind_map_fixed.py",
            "test_final_mind_map_new.py",
            "test_imports_quick.py",
            "test_json.py",
            "test_lesson_loading.py",
            "test_lesson_progress_sync.py",
            "test_mind_map.py",
            "test_mind_map_learning_sections.py",
            "test_mind_map_logic.py",
            "test_mind_map_system.py",
            "test_mind_map_system_fixed.py",
            "test_mind_map_system_new.py",
            "test_profile_debug.py",
            "test_profile_fix.py",
            "test_profile_neuroleader.py",
            "test_progress_bar.py",
            "test_refactoring.py",
            "test_tab4_direct.py",
            "test_timestamp_system.py",
            "test_updated_course_structure.py",
            "test_xp_fix_final.py",
            "test_xp_percentage_system.py",
            "test_xp_system.py"
        ],
        
        "debug_files": [
            "debug_100xp_lesson.py",
            "debug_fragment_progress.py",
            "debug_profile_neuroleader.py",
            "debug_xp_calculation.py"
        ],
        
        "simple_test_files": [
            "simple_badge_test.py",
            "simple_badge_test_final.py",
            "simple_course_test.py",
            "simple_final_test.py",
            "simple_migration_test.py",
            "simple_mind_map_test.py",
            "simple_test.py",
            "simple_test_75_percent.py"
        ],
        
        "quick_test_files": [
            "quick_badge_test.py",
            "quick_badge_timestamp_test.py",
            "quick_mind_map_test.py",
            "quick_test.py",
            "quick_user_check.py",
            "quick_verification.py"
        ],
        
        "verification_files": [
            "verify_final_fixes.py",
            "verify_fix.py", 
            "verify_migration.py",
            "verify_profile_logic.py"
        ],
        
        "final_validation_files": [
            "final_badge_integration_test.py",
            "final_badge_verification.py",
            "final_json_verification.py",
            "final_mind_map_verification.py",
            "final_verification.py",
            "final_verification_summary.py"
        ],
        
        "backup_files": [
            "views/lesson.py.backup",
            "views/degen_test_backup.py",
            "views/degen_explorer_backup.py"
        ],
        
        "fixed_alternative_files": [
            "views/degen_types_fixed.py",
            "views/degen_test_new.py",
            "main.py.broken"
        ],
        
        "utility_migration_files": [
            "fix_files.py",
            "fix_json_quotes.py",
            "validate_json.py",
            "validate_migration.py",
            "simulate_profile_logic.py",
            "profile_simulation.py",
            "IMPLEMENTATION_VERIFICATION.py"
        ],
        
        "admin_dev_files": [
            "admin_test.py",
            "direct_badge_test.py",
            "badge_test_fix.py"
        ],
        
        "syntax_check_files": [
            "syntax_check.py",
            "check_app_health.py"
        ],
        
        "documentation_files": [
            "75_PERCENT_REQUIREMENT_COMPLETE.md",
            "BADGE_ALGORITHMS_COMPLETION_SUMMARY.md",
            "BADGE_CATEGORIES_DISPLAY_FIX_COMPLETE.md",
            "BADGE_CATEGORIES_IMPLEMENTATION_COMPLETE.md",
            "BADGE_INTEGRATION_FINAL_STATUS.md",
            "COURSE_MAP_BUGS_FIXED.md",
            "COURSE_MAP_DISPLAY_FIXES_COMPLETE.md",
            "COURSE_MAP_IMPLEMENTATION_COMPLETE.md",
            "course_map_integration_demo.html",
            "COURSE_MAP_PHYSICS_FIX_COMPLETE.md",
            "COURSE_MAP_RESPONSIVE_COLORS_FIXED.md",
            "COURSE_MAP_USER_GUIDE.md",
            "DASHBOARD_NEUROLEADER_IMPLEMENTATION_COMPLETE.md",
            "JSON_SYNTAX_FIX_COMPLETE.md",
            "MIND_MAP_IMPLEMENTATION.md",
            "MIND_MAP_IMPLEMENTATION_COMPLETE.md",
            "MIND_MAP_IMPLEMENTATION_FINAL.md",
            "MIND_MAP_QUICK_START.md",
            "MIND_MAP_USER_GUIDE.md",
            "NEUROLEADERSHIP_BADGES_UPDATE.md",
            "NEUROLEADERSHIP_MIGRATION_COMPLETE.md",
            "OPENING_QUIZ_DIAGNOSTIC_COMPLETE.md",
            "PROGRESS_BAR_UPDATE_SUMMARY.md",
            "REFACTORING_SUMMARY.md",
            "XP_FIXES_COMPLETION_SUMMARY.md",
            "FINAL_COMPLETION_SUMMARY.md"
        ],
        
        "log_files": [
            "app.log"
        ]
    }
    
    # Create backup directory
    backup_dir = create_backup_directory()
    print(f"📁 Created backup directory: {backup_dir}")
    
    # Process each category
    total_moved = 0
    total_failed = 0
    
    for category, files in files_to_remove.items():
        print(f"\n🗂️  Processing {category}...")
        moved, failed = move_files_to_backup(files, backup_dir)
        
        if moved:
            print(f"  ✅ Moved {len(moved)} files")
            for file in moved:
                print(f"    - {file}")
        
        if failed:
            print(f"  ❌ Failed to move {len(failed)} files")
            for file, error in failed:
                print(f"    - {file}: {error}")
        
        total_moved += len(moved)
        total_failed += len(failed)
    
    # Clean up __pycache__ directories
    print(f"\n🗑️  Cleaning up __pycache__ directories...")
    pycache_removed = 0
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"  ✅ Removed: {pycache_path}")
                pycache_removed += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {pycache_path}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CLEANUP SUMMARY")
    print(f"Files moved to backup: {total_moved}")
    print(f"Failed to move: {total_failed}")
    print(f"__pycache__ directories removed: {pycache_removed}")
    print(f"Backup location: {backup_dir}")
    
    # Show remaining core files
    print(f"\n✅ CORE APPLICATION FILES (kept):")
    core_files = [
        "main.py",
        "requirements.txt", 
        "runtime.txt",
        "run_app.py",
        "users_data.json"
    ]
    
    core_dirs = [
        "views/",
        "utils/",
        "data/", 
        "config/",
        "static/",
        "assets/"
    ]
    
    for file in core_files:
        if os.path.exists(file):
            print(f"  📄 {file}")
    
    for dir_name in core_dirs:
        if os.path.exists(dir_name):
            print(f"  📁 {dir_name}")
    
    print(f"\n🎉 Cleanup completed! Your workspace is now organized.")
    print(f"💡 If you need any files back, they're safely stored in: {backup_dir}")

if __name__ == "__main__":
    main()
