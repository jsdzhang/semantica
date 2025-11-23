# Remove all mkdocstrings directives from reference docs
# These are causing griffe alias resolution errors

$files = Get-ChildItem "c:\Users\Mohd Kaif\semantica\docs\reference\*.md"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Remove mkdocstrings directives (:::semantica.module.Class blocks)
    $content = $content -replace '(?m)^::: semantica\.[^\r\n]+\r?\n(?:    options:\r?\n(?:      [^\r\n]+\r?\n)*)?', ''
    
    # Clean up extra blank lines
    $content = $content -replace '(\r?\n){4,}', "`r`n`r`n`r`n"
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Processed: $($file.Name)"
}

Write-Host "`nDone! All mkdocstrings directives removed."
