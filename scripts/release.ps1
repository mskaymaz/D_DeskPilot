param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$Notes,
    [string]$NotesFile,
    [switch]$Overwrite
)

$ErrorActionPreference = "Stop"

if ($Notes -and $NotesFile) {
    throw "Use either -Notes or -NotesFile, not both."
}

# Ensure clean working tree
$gitStatus = git status --porcelain
if ($LASTEXITCODE -ne 0) {
    throw "git status failed. Is git available?"
}
if ($gitStatus) {
    throw "Working tree is not clean. Commit or stash before release."
}

# Ensure gh auth
gh auth status | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI not logged in. Run: gh auth login"
}

$versionForExe = $Version
if ($versionForExe -match '^V2\.') {
    $versionForExe = $versionForExe -replace '^V2\.', ''
}
$exeName = "DigitalSaatV2.$versionForExe"
$exePath = "dist\$exeName.exe"

try {
    $env:DS_EXE_NAME = $exeName
    pyinstaller digitalSaat.spec
} finally {
    Remove-Item Env:DS_EXE_NAME -ErrorAction SilentlyContinue
}

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed."
}
if (-not (Test-Path $exePath)) {
    throw "Exe not found: $exePath"
}

# Overwrite existing tag/release if requested
$tagExists = git tag -l $Version
if ($tagExists) {
    if (-not $Overwrite) {
        throw "Tag $Version already exists. Use -Overwrite to replace it."
    }

    gh release view $Version | Out-Null
    if ($LASTEXITCODE -eq 0) {
        gh release delete $Version -y
    }

    git tag -d $Version | Out-Null
    git push origin ":refs/tags/$Version" | Out-Null
}

git tag -a $Version -m $Version
git push origin $Version

if ($NotesFile) {
    gh release create $Version $exePath --title $Version --notes-file $NotesFile
} elseif ($Notes) {
    gh release create $Version $exePath --title $Version --notes $Notes
} else {
    gh release create $Version $exePath --title $Version --notes "Windows exe: $exeName.exe"
}

Write-Host "Release complete: $Version"
