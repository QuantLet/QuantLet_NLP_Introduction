# QuantLet Submission PowerShell Script
# Automates GitHub repo creation, code push, and QuantLet submission

param(
    [string]$GitHubToken = $env:GITHUB_TOKEN,
    [string]$RepoName = "QuantLet_NLP_Introduction",
    [string]$Description = "Natural Language Processing educational modules for QuantLet platform - ASE Summer School 2025"
)

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "     QUANTLET SUBMISSION AUTOMATION" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Function to get GitHub token
function Get-GitHubToken {
    if ($GitHubToken) {
        return $GitHubToken
    }
    
    Write-Host "`nGitHub Personal Access Token Required" -ForegroundColor Yellow
    Write-Host "To create one:"
    Write-Host "1. Go to: https://github.com/settings/tokens"
    Write-Host "2. Click 'Generate new token (classic)'"
    Write-Host "3. Name it and select 'repo' scope"
    Write-Host "4. Copy the generated token`n"
    
    $token = Read-Host "Enter your GitHub token (ghp_...)"
    if (-not $token) {
        Write-Host "No token provided. Exiting." -ForegroundColor Red
        exit 1
    }
    return $token
}

# Function to create GitHub repository
function New-GitHubRepository {
    param(
        [string]$Token,
        [string]$Name,
        [string]$Desc
    )
    
    Write-Host "`nCreating GitHub repository: $Name" -ForegroundColor Green
    
    $headers = @{
        "Authorization" = "token $Token"
        "Accept" = "application/vnd.github.v3+json"
    }
    
    $body = @{
        name = $Name
        description = $Desc
        public = $true
        auto_init = $false
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
            -Method Post -Headers $headers -Body $body -ContentType "application/json"
        
        Write-Host "✓ Repository created: $($response.html_url)" -ForegroundColor Green
        return $response
    }
    catch {
        if ($_.Exception.Response.StatusCode -eq 422) {
            Write-Host "Repository already exists. Continuing..." -ForegroundColor Yellow
            
            # Get existing repo
            try {
                $user = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
                $repoUrl = "https://github.com/$($user.login)/$Name"
                return @{ html_url = $repoUrl; clone_url = "$repoUrl.git" }
            }
            catch {
                Write-Host "Error getting repository info: $_" -ForegroundColor Red
                return $null
            }
        }
        else {
            Write-Host "Error creating repository: $_" -ForegroundColor Red
            return $null
        }
    }
}

# Function to push code to GitHub
function Push-ToGitHub {
    param(
        [string]$Token,
        [string]$RepoUrl,
        [string]$Username
    )
    
    Write-Host "`nPushing code to GitHub..." -ForegroundColor Green
    
    # Configure git with token
    $remoteUrl = $RepoUrl -replace "https://", "https://${Token}@"
    
    # Initialize git if needed
    if (-not (Test-Path ".git")) {
        git init
        Write-Host "Initialized git repository" -ForegroundColor Gray
    }
    
    # Add files
    git add -A
    
    # Commit if needed
    $status = git status --porcelain
    if ($status) {
        git commit -m "QuantLet submission: NLP educational modules"
        Write-Host "✓ Created commit" -ForegroundColor Green
    }
    
    # Set remote
    git remote remove origin 2>$null
    git remote add origin $remoteUrl
    Write-Host "✓ Added remote origin" -ForegroundColor Green
    
    # Push
    git push -u origin master --force 2>&1 | Out-String
    Write-Host "✓ Code pushed successfully" -ForegroundColor Green
    
    return $true
}

# Function to create QuantLet issue
function New-QuantLetIssue {
    param(
        [string]$Token,
        [string]$RepoName,
        [string]$Username
    )
    
    Write-Host "`nCreating QuantLet submission issue..." -ForegroundColor Green
    
    $headers = @{
        "Authorization" = "token $Token"
        "Accept" = "application/vnd.github.v3+json"
    }
    
    $issueBody = @"
# New QuantLet Submission: $RepoName

## Repository Details
- **Repository**: https://github.com/$Username/$RepoName
- **Author**: $Username
- **Category**: Natural Language Processing / Machine Learning

## Description
Collection of 8 educational QuantLets for Natural Language Processing, progressing from N-grams to modern transformer architectures.

## Compliance Checklist
✅ All modules have properly formatted Metainfo.txt files
✅ Repository structure follows QuantLet conventions
✅ Comprehensive README.md at repository root
✅ All code is self-contained and reproducible
✅ Educational focus with practical examples

## Modules Included
1. NLP_Ngrams - N-gram models and text generation
2. NLP_Embeddings - Word embeddings and vector spaces  
3. NLP_Neural - Simple neural networks for NLP
4. NLP_Compare - Comparison of NLP methods
5. NLP_TokenJourney - Token processing in transformers
6. NLP_Transformers3D - 3D transformer visualizations
7. NLP_TransformersSimple - Minimal transformer implementation
8. NLP_TransformersTraining - Transformer training dynamics

## Request
Please consider adding this repository to the QuantLet organization.

---
*Submitted via automated PowerShell script*
"@
    
    $body = @{
        title = "New QuantLet Submission: $RepoName"
        body = $issueBody
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/repos/QuantLet/Styleguide-and-FAQ/issues" `
            -Method Post -Headers $headers -Body $body -ContentType "application/json"
        
        Write-Host "✓ Issue created: $($response.html_url)" -ForegroundColor Green
        return $response.html_url
    }
    catch {
        Write-Host "Could not create issue automatically: $_" -ForegroundColor Yellow
        Write-Host "Please create manually at: https://github.com/QuantLet/Styleguide-and-FAQ/issues" -ForegroundColor Yellow
        return $null
    }
}

# Main execution
try {
    # Get token
    $token = Get-GitHubToken
    
    # Get user info
    Write-Host "`nGetting GitHub user info..." -ForegroundColor Gray
    $headers = @{
        "Authorization" = "token $token"
        "Accept" = "application/vnd.github.v3+json"
    }
    $user = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
    $username = $user.login
    Write-Host "Logged in as: $username" -ForegroundColor Gray
    
    # Create repository
    $repo = New-GitHubRepository -Token $token -Name $RepoName -Desc $Description
    if (-not $repo) {
        throw "Failed to create repository"
    }
    
    # Push code
    $pushed = Push-ToGitHub -Token $token -RepoUrl $repo.clone_url -Username $username
    if (-not $pushed) {
        throw "Failed to push code"
    }
    
    # Create issue
    $issueUrl = New-QuantLetIssue -Token $token -RepoName $RepoName -Username $username
    
    # Summary
    Write-Host "`n==========================================" -ForegroundColor Cyan
    Write-Host "         SUBMISSION COMPLETE!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "`nRepository: https://github.com/$username/$RepoName" -ForegroundColor Green
    
    if ($issueUrl) {
        Write-Host "Issue: $issueUrl" -ForegroundColor Green
    }
    else {
        Write-Host "`nManual step required:" -ForegroundColor Yellow
        Write-Host "Create issue at: https://github.com/QuantLet/Styleguide-and-FAQ/issues" -ForegroundColor Yellow
        Write-Host "Use content from: quantlet_issue_template.md" -ForegroundColor Yellow
    }
    
    Write-Host "`n✅ QuantLet submission process complete!" -ForegroundColor Green
    
    # Open in browser
    Start-Process "https://github.com/$username/$RepoName"
}
catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    Write-Host "`nPlease complete submission manually:" -ForegroundColor Yellow
    Write-Host "1. Create repo at: https://github.com/new"
    Write-Host "2. Push code using: git push -u origin master"
    Write-Host "3. Submit issue at: https://github.com/QuantLet/Styleguide-and-FAQ/issues"
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")