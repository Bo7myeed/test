#!/usr/bin/env python3
"""
Directory Comparison Tool
Comprehensive comparison of two directory structures including files and content.
"""

import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict
import difflib

class DirectoryComparator:
    def __init__(self, dir1, dir2):
        self.dir1 = Path(dir1)
        self.dir2 = Path(dir2)
        self.differences = {
            'only_in_dir1': [],
            'only_in_dir2': [],
            'different_content': [],
            'identical_files': [],
            'size_differences': [],
            'summary': {}
        }
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_relative_path(self, filepath, base_dir):
        """Get relative path from base directory"""
        return filepath.relative_to(base_dir)
    
    def collect_files(self, directory):
        """Collect all files in directory with their properties"""
        files_info = {}
        if not directory.exists():
            return files_info
            
        for root, dirs, files in os.walk(directory):
            root_path = Path(root)
            for file in files:
                filepath = root_path / file
                rel_path = self.get_relative_path(filepath, directory)
                
                try:
                    stat_info = filepath.stat()
                    files_info[str(rel_path)] = {
                        'full_path': filepath,
                        'size': stat_info.st_size,
                        'hash': self.get_file_hash(filepath)
                    }
                except Exception as e:
                    files_info[str(rel_path)] = {
                        'full_path': filepath,
                        'size': 0,
                        'hash': f"Error: {str(e)}"
                    }
        
        return files_info
    
    def compare_text_files(self, file1, file2):
        """Compare text files line by line for detailed diff"""
        try:
            with open(file1, 'r', encoding='utf-8') as f1:
                lines1 = f1.readlines()
            with open(file2, 'r', encoding='utf-8') as f2:
                lines2 = f2.readlines()
            
            diff = list(difflib.unified_diff(
                lines1, lines2, 
                fromfile=str(file1), tofile=str(file2), 
                lineterm=''))
            
            return diff if diff else None
        except:
            return None
    
    def is_text_file(self, filepath):
        """Check if file is likely a text file"""
        text_extensions = {'.json', '.txt', '.yml', '.yaml', '.md', '.xml', '.csv', '.log', '.py', '.js', '.css', '.html', '.htm'}
        return filepath.suffix.lower() in text_extensions
    
    def compare_directories(self):
        """Main comparison function"""
        print(f"Comparing directories:")
        print(f"Directory 1: {self.dir1}")
        print(f"Directory 2: {self.dir2}")
        print("-" * 80)
        
        # Collect file information from both directories
        files1 = self.collect_files(self.dir1)
        files2 = self.collect_files(self.dir2)
        
        all_files = set(files1.keys()) | set(files2.keys())
        
        # Compare each file
        for rel_path in sorted(all_files):
            if rel_path in files1 and rel_path in files2:
                # File exists in both directories
                file1_info = files1[rel_path]
                file2_info = files2[rel_path]
                
                if file1_info['hash'] == file2_info['hash']:
                    self.differences['identical_files'].append(rel_path)
                else:
                    diff_info = {
                        'path': rel_path,
                        'dir1_size': file1_info['size'],
                        'dir2_size': file2_info['size'],
                        'dir1_hash': file1_info['hash'],
                        'dir2_hash': file2_info['hash']
                    }
                    
                    # For text files, add line-by-line diff
                    if self.is_text_file(Path(rel_path)):
                        diff_lines = self.compare_text_files(
                            file1_info['full_path'], 
                            file2_info['full_path']
                        )
                        if diff_lines:
                            diff_info['text_diff'] = diff_lines
                    
                    self.differences['different_content'].append(diff_info)
                    
                    if file1_info['size'] != file2_info['size']:
                        self.differences['size_differences'].append({
                            'path': rel_path,
                            'dir1_size': file1_info['size'],
                            'dir2_size': file2_info['size']
                        })
            
            elif rel_path in files1:
                # File only in directory 1
                self.differences['only_in_dir1'].append({
                    'path': rel_path,
                    'size': files1[rel_path]['size']
                })
            
            else:
                # File only in directory 2
                self.differences['only_in_dir2'].append({
                    'path': rel_path,
                    'size': files2[rel_path]['size']
                })
        
        # Generate summary
        self.differences['summary'] = {
            'total_files_dir1': len(files1),
            'total_files_dir2': len(files2),
            'identical_files': len(self.differences['identical_files']),
            'different_files': len(self.differences['different_content']),
            'only_in_dir1': len(self.differences['only_in_dir1']),
            'only_in_dir2': len(self.differences['only_in_dir2'])
        }
    
    def print_results(self):
        """Print comparison results"""
        print("\n" + "="*80)
        print("DIRECTORY COMPARISON RESULTS")
        print("="*80)
        
        # Summary
        summary = self.differences['summary']
        print(f"\nSUMMARY:")
        print(f"Files in {self.dir1.name}: {summary['total_files_dir1']}")
        print(f"Files in {self.dir2.name}: {summary['total_files_dir2']}")
        print(f"Identical files: {summary['identical_files']}")
        print(f"Different files: {summary['different_files']}")
        print(f"Only in {self.dir1.name}: {summary['only_in_dir1']}")
        print(f"Only in {self.dir2.name}: {summary['only_in_dir2']}")
        
        # Files only in directory 1
        if self.differences['only_in_dir1']:
            print(f"\n📁 FILES ONLY IN {self.dir1.name.upper()}:")
            for file_info in self.differences['only_in_dir1']:
                print(f"  - {file_info['path']} ({file_info['size']} bytes)")
        
        # Files only in directory 2
        if self.differences['only_in_dir2']:
            print(f"\n📁 FILES ONLY IN {self.dir2.name.upper()}:")
            for file_info in self.differences['only_in_dir2']:
                print(f"  - {file_info['path']} ({file_info['size']} bytes)")
        
        # Files with different content
        if self.differences['different_content']:
            print(f"\n🔄 FILES WITH DIFFERENT CONTENT:")
            for diff_info in self.differences['different_content']:
                print(f"\n  📄 {diff_info['path']}")
                print(f"    {self.dir1.name}: {diff_info['dir1_size']} bytes (hash: {diff_info['dir1_hash'][:16]}...)")
                print(f"    {self.dir2.name}: {diff_info['dir2_size']} bytes (hash: {diff_info['dir2_hash'][:16]}...)")
                
                # Show text diff for small text files
                if 'text_diff' in diff_info and len(diff_info['text_diff']) < 50:
                    print("    Differences:")
                    for line in diff_info['text_diff'][:20]:  # Show first 20 lines
                        if line.startswith('@@'):
                            print(f"      {line.strip()}")
                        elif line.startswith('-'):
                            print(f"      {line.strip()}")
                        elif line.startswith('+'):
                            print(f"      {line.strip()}")
        
        # Identical files summary
        if self.differences['identical_files']:
            print(f"\n✅ IDENTICAL FILES ({len(self.differences['identical_files'])}):")
            for filepath in self.differences['identical_files'][:10]:  # Show first 10
                print(f"  - {filepath}")
            if len(self.differences['identical_files']) > 10:
                print(f"  ... and {len(self.differences['identical_files']) - 10} more")
        
        print("\n" + "="*80)
        
        # Overall conclusion
        total_differences = (
            len(self.differences['only_in_dir1']) + 
            len(self.differences['only_in_dir2']) + 
            len(self.differences['different_content'])
        )
        
        if total_differences == 0:
            print("🎉 CONCLUSION: The directories are IDENTICAL!")
        else:
            print(f"❗ CONCLUSION: Found {total_differences} differences between the directories.")
        
        print("="*80)


def main():
    """Main function to run the comparison"""
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python directory_comparison.py <directory1> <directory2>")
        print("Example: python directory_comparison.py ModelEngine ModelEngine2")
        sys.exit(1)
    
    dir1 = sys.argv[1]
    dir2 = sys.argv[2]
    
    if not os.path.exists(dir1):
        print(f"Error: Directory '{dir1}' does not exist")
        sys.exit(1)
    
    if not os.path.exists(dir2):
        print(f"Error: Directory '{dir2}' does not exist")
        sys.exit(1)
    
    comparator = DirectoryComparator(dir1, dir2)
    comparator.compare_directories()
    comparator.print_results()


if __name__ == "__main__":
    main()