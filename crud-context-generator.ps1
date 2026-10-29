$ErrorActionPreference = 'Stop'

$out = 'tmp.txt'
$withDatabase = $false

foreach ($argument in $args) {
    switch -Exact ($argument) {
        '--with-database' {
            $withDatabase = $true
        }
        default {
            throw "Nieznany argument: $argument"
        }
    }
}

if ($withDatabase) {
    Get-Content -LiteralPath 'schema.sql'
}

Write-Output "`n"

$targets = @(
    @{ Path = 'operations/user';       Filter = '*.py' }
    @{ Path = 'routes/user';           Filter = '*.py' }
    @{ Path = 'templates/admin/users'; Filter = '*.html' }
)

foreach ($target in $targets) {
    Get-ChildItem -LiteralPath $target.Path -Recurse -File -Filter $target.Filter |
        ForEach-Object {
            Write-Output "==> $($_.FullName) <=="
            Get-Content -LiteralPath $_.FullName
            Write-Output ''
        }
}