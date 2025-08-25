#!/usr/bin/env python3
"""
QuantLet Auto-Submit Tool
Automates the process of creating GitHub repos, pushing code, and submitting to QuantLet.

Usage:
    python quantlet_auto_submit.py --token YOUR_GITHUB_TOKEN
    
Prerequisites:
    pip install requests gitpython PyGithub
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
    from github import Github
    import git
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "PyGithub", "gitpython"])
    import requests
    from github import Github
    import git


class QuantLetSubmitter:
    """Automates QuantLet submission process"""
    
    def __init__(self, github_token: str, repo_path: str = "."):
        """
        Initialize the submitter with GitHub token and repository path
        
        Args:
            github_token: Personal Access Token from GitHub
            repo_path: Path to the local repository
        """
        self.token = github_token
        self.repo_path = Path(repo_path).resolve()
        self.github = Github(github_token)
        self.user = self.github.get_user()
        
    def create_github_repository(self, 
                                  repo_name: str, 
                                  description: str,
                                  public: bool = True) -> str:
        """
        Create a new GitHub repository
        
        Args:
            repo_name: Name of the repository
            description: Repository description
            public: Whether repo should be public
            
        Returns:
            URL of the created repository
        """
        print(f"Creating GitHub repository: {repo_name}")
        
        try:
            # Check if repo already exists
            try:
                existing_repo = self.user.get_repo(repo_name)
                print(f"Repository {repo_name} already exists at {existing_repo.html_url}")
                return existing_repo.html_url
            except:
                pass  # Repo doesn't exist, create it
            
            # Create new repository
            repo = self.user.create_repo(
                name=repo_name,
                description=description,
                private=not public,
                auto_init=False  # Don't initialize with README
            )
            
            print(f"[OK] Repository created: {repo.html_url}")
            return repo.html_url
            
        except Exception as e:
            print(f"Error creating repository: {e}")
            return None
    
    def push_to_github(self, repo_name: str) -> bool:
        """
        Push local repository to GitHub
        
        Args:
            repo_name: Name of the GitHub repository
            
        Returns:
            True if successful, False otherwise
        """
        print(f"Pushing code to GitHub repository: {repo_name}")
        
        try:
            # Initialize git repo if needed
            try:
                repo = git.Repo(self.repo_path)
            except:
                repo = git.Repo.init(self.repo_path)
                print("Initialized git repository")
            
            # Add all files if not already staged
            repo.git.add(A=True)
            
            # Commit if there are changes
            if repo.is_dirty():
                repo.index.commit("Initial commit for QuantLet submission")
                print("[OK] Created commit")
            
            # Set remote
            remote_url = f"https://{self.token}@github.com/{self.user.login}/{repo_name}.git"
            
            # Remove existing origin if exists
            try:
                origin = repo.remote("origin")
                origin.remove(repo, "origin")
            except:
                pass
            
            # Add new origin
            origin = repo.create_remote("origin", remote_url)
            print(f"[OK] Added remote: {self.user.login}/{repo_name}")
            
            # Push to GitHub
            print("Pushing to GitHub...")
            origin.push(refspec="master:master", force=True)
            print("[OK] Code pushed successfully")
            
            return True
            
        except Exception as e:
            print(f"Error pushing to GitHub: {e}")
            return False
    
    def create_quantlet_issue(self, repo_name: str) -> str:
        """
        Create submission issue on QuantLet/Styleguide-and-FAQ
        
        Args:
            repo_name: Name of your repository
            
        Returns:
            URL of the created issue
        """
        print("Creating QuantLet submission issue...")
        
        try:
            # Get QuantLet Styleguide repository
            quantlet_repo = self.github.get_repo("QuantLet/Styleguide-and-FAQ")
            
            # Prepare issue content
            issue_title = f"New QuantLet Submission: {repo_name}"
            issue_body = self._generate_issue_content(repo_name)
            
            # Create issue
            issue = quantlet_repo.create_issue(
                title=issue_title,
                body=issue_body
            )
            
            print(f"[OK] Issue created: {issue.html_url}")
            return issue.html_url
            
        except Exception as e:
            print(f"Error creating issue: {e}")
            print("You may need to manually create the issue at:")
            print("https://github.com/QuantLet/Styleguide-and-FAQ/issues")
            return None
    
    def _generate_issue_content(self, repo_name: str) -> str:
        """Generate issue content for QuantLet submission"""
        
        # Try to read local metadata
        readme_path = self.repo_path / "README.md"
        description = "Educational QuantLet modules"
        
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                for line in lines:
                    if line.strip() and not line.startswith("#"):
                        description = line.strip()
                        break
        
        content = f"""# New QuantLet Submission: {repo_name}

## Repository Details
- **Repository**: https://github.com/{self.user.login}/{repo_name}
- **Author**: {self.user.name or self.user.login}
- **Category**: Natural Language Processing / Machine Learning

## Description
{description}

## Compliance Checklist
- All modules have properly formatted `Metainfo.txt` files
- Repository structure follows QuantLet conventions
- Comprehensive README.md at repository root
- All code is self-contained and reproducible
- Educational focus with practical examples

## Request
Please consider adding this repository to the QuantLet organization.

Thank you for maintaining this valuable educational resource!

---
*Submitted via QuantLet Auto-Submit Tool*
"""
        return content
    
    def verify_quantlet_structure(self) -> bool:
        """
        Verify that the repository follows QuantLet structure
        
        Returns:
            True if structure is valid
        """
        print("Verifying QuantLet structure...")
        
        issues = []
        
        # Check for README
        if not (self.repo_path / "README.md").exists():
            issues.append("Missing README.md")
        
        # Check for Metainfo files
        metainfo_count = 0
        for metainfo in self.repo_path.rglob("Metainfo.txt"):
            metainfo_count += 1
            
            # Basic validation of Metainfo content
            with open(metainfo, 'r', encoding='utf-8') as f:
                content = f.read()
                required_fields = ["Name of QuantLet", "Published in", 
                                   "Description", "Keywords", "Author"]
                for field in required_fields:
                    if field not in content:
                        issues.append(f"Missing '{field}' in {metainfo}")
        
        if metainfo_count == 0:
            issues.append("No Metainfo.txt files found")
        
        if issues:
            print("[WARNING] Structure issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        print(f"[OK] Structure verified: {metainfo_count} QuantLet(s) found")
        return True
    
    def full_submission_workflow(self, 
                                  repo_name: str = "QuantLet_NLP_Introduction",
                                  description: str = None) -> Dict[str, Any]:
        """
        Execute the complete submission workflow
        
        Args:
            repo_name: GitHub repository name
            description: Repository description
            
        Returns:
            Dictionary with submission results
        """
        if description is None:
            description = "Natural Language Processing educational modules for QuantLet platform"
        
        results = {
            "verified": False,
            "repo_created": False,
            "pushed": False,
            "issue_created": False,
            "repo_url": None,
            "issue_url": None
        }
        
        print("\n" + "="*60)
        print("QUANTLET AUTOMATIC SUBMISSION TOOL")
        print("="*60 + "\n")
        
        # Step 1: Verify structure
        results["verified"] = self.verify_quantlet_structure()
        if not results["verified"]:
            print("\n[WARNING] Fix structure issues before proceeding")
            return results
        
        # Step 2: Create GitHub repository
        repo_url = self.create_github_repository(repo_name, description)
        if repo_url:
            results["repo_created"] = True
            results["repo_url"] = repo_url
        else:
            print("\n[ERROR] Failed to create repository")
            return results
        
        # Wait a moment for GitHub to process
        time.sleep(2)
        
        # Step 3: Push code
        results["pushed"] = self.push_to_github(repo_name)
        if not results["pushed"]:
            print("\n[ERROR] Failed to push code")
            return results
        
        # Step 4: Create QuantLet issue
        issue_url = self.create_quantlet_issue(repo_name)
        if issue_url:
            results["issue_created"] = True
            results["issue_url"] = issue_url
        
        # Summary
        print("\n" + "="*60)
        print("SUBMISSION SUMMARY")
        print("="*60)
        print(f"[OK] Repository: {results['repo_url']}")
        if results["issue_url"]:
            print(f"[OK] Issue: {results['issue_url']}")
        else:
            print("[WARNING] Manual issue creation needed at:")
            print("  https://github.com/QuantLet/Styleguide-and-FAQ/issues")
        print("\n[SUCCESS] QuantLet submission process complete!")
        
        return results


def main():
    """Main entry point for the script"""
    
    parser = argparse.ArgumentParser(
        description="Automate QuantLet submission to GitHub"
    )
    parser.add_argument(
        "--token", "-t",
        help="GitHub Personal Access Token (or set GITHUB_TOKEN env variable)",
        default=os.getenv("GITHUB_TOKEN")
    )
    parser.add_argument(
        "--repo-name", "-r",
        help="Repository name",
        default="QuantLet_NLP_Introduction"
    )
    parser.add_argument(
        "--description", "-d",
        help="Repository description",
        default="Natural Language Processing educational modules for QuantLet platform"
    )
    parser.add_argument(
        "--path", "-p",
        help="Path to local repository",
        default="."
    )
    
    args = parser.parse_args()
    
    if not args.token:
        print("\n[ERROR] GitHub token required!")
        print("\nHow to get a token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Give it a name and select 'repo' scope")
        print("4. Copy the token and run:")
        print("   python quantlet_auto_submit.py --token YOUR_TOKEN")
        print("\nOr set environment variable:")
        print("   Windows: set GITHUB_TOKEN=your_token_here")
        print("   Linux/Mac: export GITHUB_TOKEN=your_token_here")
        sys.exit(1)
    
    # Create submitter and run workflow
    submitter = QuantLetSubmitter(args.token, args.path)
    results = submitter.full_submission_workflow(args.repo_name, args.description)
    
    # Exit with appropriate code
    if results["issue_created"]:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()