$ErrorActionPreference = 'Stop'
$folder = Join-Path $PSScriptRoot ('diagnose-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $folder | Out-Null
$client = [Net.Sockets.TcpClient]::new()
try {
    $client.Connect('127.0.0.1', 17979)
    $client.ReceiveTimeout = 30000
    $stream = $client.GetStream()
    $reader = [IO.StreamReader]::new($stream)
    $writer = [IO.StreamWriter]::new($stream, [Text.UTF8Encoding]::new($false))
    $writer.AutoFlush = $true
    $id = 0
    foreach ($request in @(
        @{method='document.inspect'; params=@{}; name='document.json'},
        @{method='ui.inspect'; params=@{}; name='ui.json'},
        @{method='engine.execute'; params=@{command='document.serialize'; params=@{format='vectorcraft'}}; name='document-data.json'},
        @{method='ui.screenshot'; params=@{path=(Join-Path $folder 'window.png')}; name='screenshot.json'}
    )) {
        $id++
        $writer.WriteLine((@{id=$id; method=$request.method; params=$request.params} | ConvertTo-Json -Depth 20 -Compress))
        $line = $reader.ReadLine()
        if (!$line) { throw 'Die App hat die Diagnoseverbindung beendet.' }
        [IO.File]::WriteAllText((Join-Path $folder $request.name), $line, [Text.UTF8Encoding]::new($false))
        if ($request.name -eq 'document-data.json') {
            $reply = $line | ConvertFrom-Json
            if ($reply.ok -and $reply.result.dataBase64) {
                [IO.File]::WriteAllBytes((Join-Path $folder 'document.vectorcraft'), [Convert]::FromBase64String($reply.result.dataBase64))
            }
        }
    }
} catch {
    $_ | Out-String | Set-Content (Join-Path $folder 'connection-error.txt')
    Write-Host 'Die App ist nicht erreichbar. Vorhandene Protokolle werden trotzdem gesichert.'
} finally {
    $client.Dispose()
    $profileRoot = if ($env:VECTORCRAFT_CONFIG_DIR) { $env:VECTORCRAFT_CONFIG_DIR } else { Join-Path $PSScriptRoot 'profile' }
    Copy-Item (Join-Path $profileRoot 'logs\*') $folder -ErrorAction SilentlyContinue
    Copy-Item (Join-Path $PSScriptRoot 'BUILD.txt') $folder -ErrorAction SilentlyContinue
    Copy-Item (Join-Path $PSScriptRoot 'SELFTEST.json') $folder -ErrorAction SilentlyContinue
}
Compress-Archive -Path "$folder\*" -DestinationPath "$folder.zip"
Write-Host "Diagnose gespeichert: $folder.zip"
