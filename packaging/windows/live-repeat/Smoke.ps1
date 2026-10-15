param([Parameter(Mandatory=$true)][string]$Exe, [Parameter(Mandatory=$true)][string]$Output)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $Output -Force | Out-Null
$env:VECTORCRAFT_CONFIG_DIR = Join-Path $Output ('profile-' + [Guid]::NewGuid().ToString('N'))
$env:RUST_LOG = 'warn,vectorcraft*=info'
$app = Start-Process -FilePath $Exe -ArgumentList '--control', '17979', '--in-window-menus' -PassThru -RedirectStandardOutput (Join-Path $Output 'stdout.log') -RedirectStandardError (Join-Path $Output 'stderr.log')
$client = $null
$script:requestId = 0
$script:transcript = [Collections.Generic.List[object]]::new()
function Request($method, $params) {
    $script:requestId++
    $req = @{id=$script:requestId; method=$method; params=$params}
    $writer.WriteLine(($req | ConvertTo-Json -Depth 30 -Compress))
    $line = $reader.ReadLine()
    if (!$line) { throw 'Control connection closed' }
    $reply = $line | ConvertFrom-Json
    $script:transcript.Add(@{request=$req; response=$reply})
    if (!$reply.ok) { throw "Control failed: $line" }
    return $reply.result
}
function Execute($command, $params) { Request 'engine.execute' @{command=$command; params=$params} }
function WaitIdle {
    $deadline = (Get-Date).AddSeconds(30)
    do {
        $state = Request 'ui.inspect' @{}
        if (@($state.background).Count -eq 0 -and @($state.opening).Count -eq 0) { return }
        Start-Sleep -Milliseconds 100
    } while ((Get-Date) -lt $deadline)
    throw 'Background save or open did not finish within 30 seconds'
}
function RepeatState($id) {
    $state = Request 'document.inspect' @{}
    $node = $state.layers[0].children | Where-Object { $_.id -eq $id }
    if (!$node.repeat) { throw 'Repeat missing or expanded' }
    return $node
}
try {
    for ($attempt=0; $attempt -lt 100; $attempt++) {
        $client = [Net.Sockets.TcpClient]::new()
        try { $client.Connect('127.0.0.1', 17979); break } catch { $client.Dispose(); $client=$null; Start-Sleep -Milliseconds 500 }
    }
    if (!$client) { throw 'Native app did not start its control server' }
    $client.ReceiveTimeout=30000
    $stream=$client.GetStream()
    $reader=[IO.StreamReader]::new($stream)
    $writer=[IO.StreamWriter]::new($stream, [Text.UTF8Encoding]::new($false))
    $writer.AutoFlush=$true
    foreach ($kind in @('radial', 'grid', 'mirror')) {
        Execute 'file.new' @{width=400; height=400} | Out-Null
        $seed=(Execute 'shape.rectangle' @{x=190; y=70; width=20; height=20}).id
        $repeat=(Execute "object.repeat.$kind" @{ids=@($seed)}).id
        $before=(RepeatState $repeat).repeat.transforms | ConvertTo-Json -Depth 10 -Compress
        Execute 'object.repeat.edit' @{id=$repeat} | Out-Null
        Request 'ui.tool.select' @{tool='rectangle'} | Out-Null
        Request 'ui.pointer' @{events=@(@{kind='down'; x=145; y=45}, @{kind='drag'; x=180; y=65}, @{kind='up'; x=180; y=65})} | Out-Null
        $after=RepeatState $repeat
        if ($after.children.Count -ne 2) { throw 'Drawing did not join source container' }
        $extra=($after.children | Where-Object { $_.id -ne $seed }).id
        $copy=(Execute 'layer.move' @{ids=@($extra); target=$repeat; place='inside'; copy=$true}).ids[0]
        if ((RepeatState $repeat).children.Count -ne 3) { throw 'Copy into repeat failed' }
        Execute 'layer.move' @{ids=@($copy); target=$seed; place='below'} | Out-Null
        if ((RepeatState $repeat).children[-1].id -ne $copy) { throw 'Source reorder failed' }
        Execute 'edit.clear' @{ids=@($copy)} | Out-Null
        if ((RepeatState $repeat).children.Count -ne 2) { throw 'Source delete failed' }
        Execute 'edit.undo' @{} | Out-Null
        if ((RepeatState $repeat).children.Count -ne 3) { throw 'Undo failed' }
        Execute 'edit.redo' @{} | Out-Null
        if ((RepeatState $repeat).children.Count -ne 2) { throw 'Redo failed' }
        if (((RepeatState $repeat).repeat.transforms | ConvertTo-Json -Depth 10 -Compress) -ne $before) { throw 'Repeat geometry moved' }
        Request 'ui.screenshot' @{path=(Join-Path $Output "$kind-editing.png")} | Out-Null
        Execute 'object.exitIsolation' @{} | Out-Null
        $path=Join-Path $Output "$kind.vectorcraft"
        Request 'app.save' @{path=$path} | Out-Null
        WaitIdle
        if (!(Test-Path $path)) { throw 'Native save did not produce a file' }
        Execute 'file.close' @{} | Out-Null
        Execute 'file.new' @{width=400; height=400} | Out-Null
        Request 'app.open' @{path=$path} | Out-Null
        WaitIdle
        if ((RepeatState $repeat).children.Count -ne 2) { throw 'Reopen lost source contents' }
        if (((RepeatState $repeat).repeat.transforms | ConvertTo-Json -Depth 10 -Compress) -ne $before) { throw 'Reopen changed arrangement' }
        Request 'ui.screenshot' @{path=(Join-Path $Output "$kind-reopened.png")} | Out-Null
    }
    @{passed=$true; commit=$env:GITHUB_SHA; version=$env:VECTORCRAFT_VERSION; platform=[Environment]::OSVersion.VersionString; executableSha256=(Get-FileHash -Algorithm SHA256 $Exe).Hash; checks=@('native startup','radial/grid/mirror','tool drawing into source','copy','reorder','delete','stable arrangement','undo','redo','save','reopen','presented screenshots')} | ConvertTo-Json | Set-Content (Join-Path $Output 'report.json')
} finally {
    $script:transcript | ConvertTo-Json -Depth 50 | Set-Content (Join-Path $Output 'transcript.json')
    if ($client) { $client.Dispose() }
    # The app may restart itself with another graphics adapter during startup.
    Get-Process -Name ([IO.Path]::GetFileNameWithoutExtension($Exe)) -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -eq $Exe } | Stop-Process -Force -ErrorAction SilentlyContinue
}
