#!/usr/bin/env python3
"""
Generate a detailed comparison report and save it to a file
"""

import json
import os
from directory_comparison import DirectoryComparator

def generate_detailed_report(dir1, dir2, output_file="comparison_report.json"):
    """Generate a detailed JSON report of directory comparison"""
    
    comparator = DirectoryComparator(dir1, dir2)
    comparator.compare_directories()
    
    # Prepare detailed report data
    report_data = {
        "comparison_info": {
            "directory1": str(comparator.dir1),
            "directory2": str(comparator.dir2),
            "timestamp": __import__('datetime').datetime.now().isoformat()
        },
        "summary": comparator.differences['summary'],
        "files_only_in_dir1": comparator.differences['only_in_dir1'],
        "files_only_in_dir2": comparator.differences['only_in_dir2'],
        "files_with_different_content": [
            {
                "path": diff['path'],
                "dir1_size": diff['dir1_size'],
                "dir2_size": diff['dir2_size'],
                "dir1_hash": diff['dir1_hash'],
                "dir2_hash": diff['dir2_hash'],
                "has_text_diff": 'text_diff' in diff
            }
            for diff in comparator.differences['different_content']
        ],
        "identical_files": comparator.differences['identical_files']
    }
    
    # Save detailed report
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"Detailed comparison report saved to: {output_file}")
    return report_data

def main():
    # Generate comparison for ModelEngine vs ModelEngine2
    report_data = generate_detailed_report("ModelEngine", "ModelEngine2", "comparison_report.json")
    
    # Also create a summary text file
    with open("comparison_summary.txt", 'w', encoding='utf-8') as f:
        f.write("DIRECTORY COMPARISON SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        
        summary = report_data['summary']
        f.write(f"Directory 1 (ModelEngine): {summary['total_files_dir1']} files\n")
        f.write(f"Directory 2 (ModelEngine2): {summary['total_files_dir2']} files\n")
        f.write(f"Identical files: {summary['identical_files']}\n")
        f.write(f"Different files: {summary['different_files']}\n")
        f.write(f"Files only in ModelEngine: {summary['only_in_dir1']}\n")
        f.write(f"Files only in ModelEngine2: {summary['only_in_dir2']}\n\n")
        
        total_differences = summary['only_in_dir1'] + summary['only_in_dir2'] + summary['different_files']
        f.write(f"Total differences found: {total_differences}\n")
        
        if total_differences == 0:
            f.write("\nCONCLUSION: The directories are IDENTICAL!\n")
        else:
            f.write(f"\nCONCLUSION: The directories have significant differences.\n")
            f.write("- ModelEngine contains many additional files not present in ModelEngine2\n")
            f.write("- There are differences in file content for some shared files\n")
    
    print("Summary text report saved to: comparison_summary.txt")

if __name__ == "__main__":
    main()