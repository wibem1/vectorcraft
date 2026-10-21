Option Explicit
Dim shell, files, folder, command
Set shell = CreateObject("WScript.Shell")
Set files = CreateObject("Scripting.FileSystemObject")
folder = files.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = folder
command = "pyw -3 " & Chr(34) & folder & "\vectorcraft_chat.py" & Chr(34)
On Error Resume Next
shell.Run command, 0, False
If Err.Number <> 0 Then
    MsgBox "Python 3 mit Tkinter wurde nicht gefunden. Bitte Python installieren oder das fertige App-Paket verwenden.", 48, "VectorCraft Chat"
End If
