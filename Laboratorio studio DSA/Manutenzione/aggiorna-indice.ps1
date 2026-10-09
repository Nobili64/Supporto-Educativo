# Compatibile con Windows PowerShell 5.1. Nessun programma esterno richiesto.
[CmdletBinding()]
param()

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
$script:OdsOffice = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
$script:OdsTable = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
$script:OdsText = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
$script:Headers = @('ID','Titolo','Materia','Argomento','Classe','Obiettivo','Tipo','Guida','Destinatario','PDF','Sorgente','Revisione','Kit','Prerequisiti','Compito','Difficolta','Strumento','Curricolo','Coorte','Fonti','Versione','Stato')
$temporaryIndex = $null

function Get-OdsRepeat {
    param([System.Xml.XmlElement]$Element, [string]$Attribute, [long]$RowNumber)
    $raw = $Element.GetAttribute($Attribute, $script:OdsTable)
    if ([string]::IsNullOrEmpty($raw)) { return [long]1 }
    $value = [long]0
    if (-not [long]::TryParse($raw, [ref]$value) -or $value -lt 1 -or $value -gt 2147483647) {
        throw "Riga $RowNumber`: ripetizione ODS non valida ($Attribute)."
    }
    return $value
}

function Get-OdsNodeText {
    param([System.Xml.XmlNode]$Node)
    $builder = New-Object System.Text.StringBuilder
    foreach ($child in $Node.ChildNodes) {
        if ($child.NodeType -eq [System.Xml.XmlNodeType]::Text -or $child.NodeType -eq [System.Xml.XmlNodeType]::CDATA) {
            [void]$builder.Append($child.Value)
        } elseif ($child.NamespaceURI -eq $script:OdsText -and $child.LocalName -eq 's') {
            $count = 1
            $raw = $child.GetAttribute('c', $script:OdsText)
            if ($raw) {
                if (-not [int]::TryParse($raw, [ref]$count) -or $count -lt 1 -or $count -gt 100000) {
                    throw 'Spaziatura ODS non valida.'
                }
            }
            [void]$builder.Append((' ' * $count))
        } elseif ($child.NamespaceURI -eq $script:OdsText -and $child.LocalName -eq 'tab') {
            [void]$builder.Append("`t")
        } elseif ($child.NamespaceURI -eq $script:OdsText -and $child.LocalName -eq 'line-break') {
            [void]$builder.Append("`n")
        } else {
            [void]$builder.Append((Get-OdsNodeText -Node $child))
        }
    }
    return $builder.ToString()
}

function Get-OdsCellValue {
    param([System.Xml.XmlElement]$Cell, [System.Xml.XmlNamespaceManager]$Namespaces, [long]$RowNumber)
    # Le formule non vengono eseguite: si legge soltanto il valore salvato nel foglio.
    $valueType = $Cell.GetAttribute('value-type', $script:OdsOffice)
    if ($valueType -eq 'date') {
        $dateValue = $Cell.GetAttribute('date-value', $script:OdsOffice)
        $parsedDate = [datetime]::MinValue
        if (-not [datetime]::TryParse($dateValue, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::RoundtripKind, [ref]$parsedDate)) {
            throw "Riga $RowNumber`: data ODS non valida '$dateValue'."
        }
        return $parsedDate.ToString('yyyy-MM-dd', [System.Globalization.CultureInfo]::InvariantCulture)
    }
    if ($Cell.HasAttribute('string-value', $script:OdsOffice)) {
        return $Cell.GetAttribute('string-value', $script:OdsOffice)
    }
    $paragraphs = @($Cell.SelectNodes('./text:p', $Namespaces))
    if ($paragraphs.Count -gt 0) {
        $texts = New-Object 'System.Collections.Generic.List[string]'
        foreach ($paragraph in $paragraphs) { $texts.Add((Get-OdsNodeText -Node $paragraph)) }
        return [string]::Join("`n", $texts.ToArray())
    }
    foreach ($attribute in @('value','boolean-value','time-value')) {
        if ($Cell.HasAttribute($attribute, $script:OdsOffice)) { return $Cell.GetAttribute($attribute, $script:OdsOffice) }
    }
    return ''
}

function Read-OdsRow {
    param([System.Xml.XmlElement]$Row, [System.Xml.XmlNamespaceManager]$Namespaces, [long]$RowNumber)
    $values = New-Object 'string[]' $script:Headers.Count
    for ($i = 0; $i -lt $values.Length; $i++) { $values[$i] = '' }
    $column = [long]0
    $hasAny = $false
    $hasExtra = $false
    foreach ($cell in $Row.SelectNodes('./table:table-cell | ./table:covered-table-cell', $Namespaces)) {
        $repeat = Get-OdsRepeat -Element $cell -Attribute 'number-columns-repeated' -RowNumber $RowNumber
        $value = [string](Get-OdsCellValue -Cell $cell -Namespaces $Namespaces -RowNumber $RowNumber)
        $value = $value.Trim()
        if ($value.Length -gt 0) {
            $hasAny = $true
            if ($column + $repeat -gt $values.Length) { $hasExtra = $true }
        }
        # Si proiettano soltanto le colonne previste: le celle vuote ripetute non sono espanse.
        $end = [math]::Min($column + $repeat, [long]$values.Length)
        for ($target = $column; $target -lt $end; $target++) { $values[[int]$target] = $value }
        $column += $repeat
    }
    return [pscustomobject]@{ Values = $values; HasAny = $hasAny; HasExtra = $hasExtra }
}

function Confirm-RelativeFile {
    param([string]$RelativePath, [string[]]$Extensions, [string]$Field, [long]$RowNumber, [string]$LibraryRoot)
    if ([string]::IsNullOrWhiteSpace($RelativePath)) { throw "Riga $RowNumber`: '$Field' e' vuoto." }
    if ([System.IO.Path]::IsPathRooted($RelativePath) -or $RelativePath.Contains(':')) {
        throw "Riga $RowNumber`: '$Field' deve essere un percorso relativo, senza indirizzi web o unita': $RelativePath"
    }
    $parts = @($RelativePath -split '[\\/]')
    $publicRoots = @("Materie","Metodo di studio","Laboratorio delle mappe","Preparazione all’esame","Modelli riutilizzabili","Guida all’uso")
    if ($publicRoots -notcontains $parts[0] -or @($parts | Where-Object { $_ -ieq 'Percorsi individuali' -or $_ -ieq 'Casi' }).Count -gt 0) {
        throw "Riga $RowNumber`: '$Field' non appartiene alla biblioteca generale. Percorsi individuali esclusi."
    }
    if ($parts.Count -eq 0 -or @($parts | Where-Object { $_ -eq '..' -or $_ -eq '' }).Count -gt 0) {
        throw "Riga $RowNumber`: '$Field' contiene un attraversamento di cartelle o un separatore non valido: $RelativePath"
    }
    $native = $RelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    try { $fullPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($LibraryRoot, $native)) }
    catch { throw "Riga $RowNumber`: percorso '$Field' non valido: $RelativePath" }
    $prefix = $LibraryRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    if (-not $fullPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Riga $RowNumber`: '$Field' esce dalla cartella del laboratorio: $RelativePath"
    }
    $extension = [System.IO.Path]::GetExtension($fullPath).ToLowerInvariant()
    if ($Extensions -notcontains $extension) { throw "Riga $RowNumber`: formato '$Field' non ammesso: $RelativePath" }
    if (-not [System.IO.File]::Exists($fullPath)) { throw "Riga $RowNumber`: file '$Field' non trovato: $RelativePath" }
    # Anche una giunzione o un collegamento simbolico potrebbe uscire dalla biblioteca.
    $current = $fullPath
    while ($current.Length -gt $LibraryRoot.Length) {
        if (([System.IO.File]::GetAttributes($current) -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Riga $RowNumber`: '$Field' attraversa un collegamento simbolico o una giunzione: $RelativePath"
        }
        $current = [System.IO.Path]::GetDirectoryName($current)
    }
    return ($RelativePath -replace '\\','/')
}

try {
    $libraryRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
    $catalogPath = Join-Path $libraryRoot 'Catalogo.ods'
    $templatePath = Join-Path $PSScriptRoot 'index-template.html'
    $indexPath = Join-Path $libraryRoot 'Indice.html'
    if (-not [System.IO.File]::Exists($catalogPath)) { throw "Catalogo non trovato: $catalogPath" }
    if (-not [System.IO.File]::Exists($templatePath)) { throw "Modello dell'indice non trovato: $templatePath" }
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = $null
    $stream = $null
    $reader = $null
    try {
        $archive = [System.IO.Compression.ZipFile]::OpenRead($catalogPath)
        $entry = $archive.GetEntry('content.xml')
        if ($null -eq $entry) { throw 'Catalogo.ods non contiene content.xml.' }
        $stream = $entry.Open()
        $settings = New-Object System.Xml.XmlReaderSettings
        $settings.DtdProcessing = [System.Xml.DtdProcessing]::Prohibit
        $settings.XmlResolver = $null
        $reader = [System.Xml.XmlReader]::Create($stream, $settings)
        $document = New-Object System.Xml.XmlDocument
        $document.XmlResolver = $null
        $document.Load($reader)
    } finally {
        if ($null -ne $reader) { $reader.Dispose() }
        if ($null -ne $stream) { $stream.Dispose() }
        if ($null -ne $archive) { $archive.Dispose() }
    }
    $namespaces = New-Object System.Xml.XmlNamespaceManager($document.NameTable)
    $namespaces.AddNamespace('office', $script:OdsOffice)
    $namespaces.AddNamespace('table', $script:OdsTable)
    $namespaces.AddNamespace('text', $script:OdsText)
    $sheets = @($document.SelectNodes('/office:document-content/office:body/office:spreadsheet/table:table', $namespaces) | Where-Object { $_.GetAttribute('name', $script:OdsTable) -ceq 'Risorse' })
    if ($sheets.Count -ne 1) { throw "Il catalogo deve contenere un unico foglio chiamato 'Risorse'." }
    $sheet = $sheets[0]
    $rows = $sheet.SelectNodes('./table:table-row | ./table:table-header-rows/table:table-row | ./table:table-row-group//table:table-row | ./table:table-rows/table:table-row', $namespaces)
    $records = New-Object 'System.Collections.Generic.List[object]'
    $ids = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    $headerFound = $false
    $rowNumber = [long]1
    foreach ($row in $rows) {
        $repeat = Get-OdsRepeat -Element $row -Attribute 'number-rows-repeated' -RowNumber $rowNumber
        $parsed = Read-OdsRow -Row $row -Namespaces $namespaces -RowNumber $rowNumber
        if (-not $parsed.HasAny) { $rowNumber += $repeat; continue }
        if (-not $headerFound) {
            if ($parsed.Values[0] -ceq 'ID') {
                for ($i = 0; $i -lt $script:Headers.Count; $i++) {
                    if ($parsed.Values[$i] -cne $script:Headers[$i]) {
                        throw "Riga $rowNumber`, colonna $($i + 1): intestazione attesa '$($script:Headers[$i])', trovata '$($parsed.Values[$i])'."
                    }
                }
                if ($parsed.HasExtra) { throw "Riga $rowNumber`: sono presenti intestazioni oltre le colonne previste previste." }
                if ($repeat -ne 1) { throw "Riga $rowNumber`: la riga delle intestazioni e' ripetuta." }
                $headerFound = $true
            }
            $rowNumber += $repeat
            continue
        }
        if ($parsed.HasExtra) { throw "Riga $rowNumber`: dati fuori dalle colonne previste del catalogo." }
        for ($i = 0; $i -lt $script:Headers.Count; $i++) {
            if ([string]::IsNullOrWhiteSpace($parsed.Values[$i])) { throw "Riga $rowNumber`: campo '$($script:Headers[$i])' obbligatorio mancante." }
        }
        if ($repeat -ne 1) { throw "Riga $rowNumber`: la riga con ID '$($parsed.Values[0])' e' ripetuta $repeat volte; ogni risorsa deve avere un ID unico." }
        if (-not $ids.Add($parsed.Values[0])) { throw "Riga $rowNumber`: ID duplicato '$($parsed.Values[0])'." }
        $record = [ordered]@{}
        for ($i = 0; $i -lt $script:Headers.Count; $i++) { $record[$script:Headers[$i]] = $parsed.Values[$i] }
        if (@('bozza','da verificare','pronto','ritirato') -cnotcontains $record['Stato']) { throw "Riga $RowNumber`: Stato non valido." }
        $record['PDF'] = Confirm-RelativeFile -RelativePath $record['PDF'] -Extensions @('.pdf') -Field 'PDF' -RowNumber $rowNumber -LibraryRoot $libraryRoot
        $record['Sorgente'] = Confirm-RelativeFile -RelativePath $record['Sorgente'] -Extensions @('.odt','.odg') -Field 'Sorgente' -RowNumber $rowNumber -LibraryRoot $libraryRoot
        $records.Add([pscustomobject]$record)
        $rowNumber += $repeat
    }
    if (-not $headerFound) { throw "Foglio Risorse: intestazioni non trovate. La prima colonna della riga delle intestazioni deve essere ID." }
    if ($records.Count -eq 0) { throw 'Il foglio Risorse non contiene risorse complete. Indice precedente conservato.' }
    $template = [System.IO.File]::ReadAllText($templatePath, [System.Text.Encoding]::UTF8)
    $token = '__CATALOG_DATA__'
    if ([regex]::Matches($template, [regex]::Escape($token)).Count -ne 1) { throw 'Il modello HTML deve contenere una sola posizione per i dati del catalogo.' }
    $ready = @($records.ToArray() | Where-Object { $_.Stato -ceq 'pronto' })
    $json = ConvertTo-Json -InputObject $ready -Depth 6 -Compress
    # Queste sostituzioni impediscono che contenuti delle celle chiudano il blocco script.
    $json = $json.Replace('<','\u003c').Replace('>','\u003e').Replace('&','\u0026').Replace([string][char]0x2028,'\u2028').Replace([string][char]0x2029,'\u2029')
    $html = $template.Replace($token, $json)
    $temporaryIndex = Join-Path $libraryRoot ('Indice.' + [guid]::NewGuid().ToString('N') + '.tmp')
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($temporaryIndex, $html, $utf8)
    # File temporaneo sullo stesso volume; l'indice esistente resta intatto fino alla sostituzione.
    if ([System.IO.File]::Exists($indexPath)) { [System.IO.File]::Replace($temporaryIndex, $indexPath, (Join-Path $PSScriptRoot 'Indice.precedente.html')) }
    else { [System.IO.File]::Move($temporaryIndex, $indexPath) }
    $temporaryIndex = $null
    Write-Host ("Indice aggiornato: {0} risorse pronte su {1}. Apri Indice.html." -f $ready.Count,$records.Count) -ForegroundColor Green
    exit 0
} catch {
    if ($temporaryIndex -and [System.IO.File]::Exists($temporaryIndex)) {
        try { [System.IO.File]::Delete($temporaryIndex) } catch { }
    }
    Write-Host ("Aggiornamento non riuscito. L'indice precedente non e' stato modificato.`n" + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
