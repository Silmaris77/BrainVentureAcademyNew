#!/usr/bin/env python3
"""
Simplified Workspace Cleanup Script for BrainVenture Academy
With output written to a log file
"""

import os
import shutil
import datetime
from pathlib import Path

# Create log file
log_file = "cleanup_log.txt"
with open(log_file, "w") as f:
    f.write("Starting cleanup process...\n")

def log(message):
    """Write to log file"""
    with open(log_file, "a") as f:
        f.write(message + "\n")
    
def main():
    log("🧹 BrainVenture Academy - Workspace Cleanup")
    log("=" * 50)
    
    # Create backup directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_cleanup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    log(f"📁 Created backup directory: {backup_dir}")
    
    # Define categories of files to clean up
    categories = {
        "Test Files": "test_*.py",
        "Debug Files": "debug_*.py",
        "Simple Test Files": "simple_*.py",
        "Quick Test Files": "quick_*.py",
        "Verification Files": "verify_*.py",
        "Documentation Files": "*.md",
        "Backup Files": "*.backup"
    }
    
    # Process each category
    total_moved = 0
    for category, pattern in categories.items():
        log(f"\n🗂️ Processing {category}...")
        
        # Find files matching pattern
        matches = []
        for root, dirs, files in os.walk("."):
            for filename in files:
                if Path(filename).match(pattern):
                    file_path = os.path.join(root, filename)
                    # Skip the backup directory itself
                    if backup_dir not in file_path and log_file not in file_path and "cleanup_" not in file_path:
                        matches.append(file_path)
        
        if not matches:
            log(f"  No files found matching {pattern}")
            continue
            
        log(f"  Found {len(matches)} files matching {pattern}")
        
        # Move files to backup
        moved = 0
        for file_path in matches:
            try:
                relative_path = os.path.relpath(file_path)
                backup_file_path = os.path.join(backup_dir, relative_path)
                backup_file_dir = os.path.dirname(backup_file_path)
                
                if not os.path.exists(backup_file_dir):
                    os.makedirs(backup_file_dir, exist_ok=True)
                
                shutil.copy2(file_path, backup_file_path)  # Copy first
                os.remove(file_path)  # Then delete original
                log(f"  ✅ Moved: {relative_path}")
                moved += 1
            except Exception as e:
                log(f"  ❌ Failed to move {file_path}: {str(e)}")
        
        total_moved += moved
    
    # Clean up __pycache__ directories
    log(f"\n🗑️ Cleaning up __pycache__ directories...")
    pycache_removed = 0
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                log(f"  ✅ Removed: {pycache_path}")
                pycache_removed += 1
            except Exception as e:
                log(f"  ❌ Failed to remove {pycache_path}: {str(e)}")
    
    # Summary
    log("\n" + "=" * 50)
    log("📊 CLEANUP SUMMARY")
    log(f"Files moved to backup: {total_moved}")
    log(f"__pycache__ directories removed: {pycache_removed}")
    log(f"Backup location: {backup_dir}")
    log(f"\n🎉 Cleanup completed! Your workspace is now organized.")
    log(f"💡 If you need any files back, they're safely stored in: {backup_dir}")
    
    # Copy log to backup
    shutil.copy2(log_file, os.path.join(backup_dir, log_file))

if __name__ == "__main__":
    main()
