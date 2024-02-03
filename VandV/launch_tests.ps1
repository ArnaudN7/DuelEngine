# Chemin vers le script de tests
$cheminScriptTest = "C:\Users\Arno\Code\DuelEngine\DuelEngine\VandV\script_verif.txt"

# Chemin vers l'exécuteur de script de tests
$cheminScriptLauncher = "C:/Program Files/Ingescape/Ingescape Circle/igs.exe"

$cheminPlateforme = "C:\Users\Arno\Code\DuelEngine\DuelEngine\DuelEngine\DuelEngine.igsplatform"

# Exécute la commande
Start-Process -FilePath $cheminScriptLauncher -ArgumentList "--script", $cheminScriptTest, "--platform", $cheminPlateforme
