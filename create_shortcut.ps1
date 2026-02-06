$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut("C:\Users\mtjon\Desktop\Newborn Navigator.lnk")
$s.TargetPath = "C:\Users\mtjon\Desktop\newborn-navigator\start_server.bat"
$s.WorkingDirectory = "C:\Users\mtjon\Desktop\newborn-navigator"
$s.Save()
Write-Host "Shortcut created on Desktop!"
