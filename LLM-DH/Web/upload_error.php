<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $target_dir = "uploads/";
    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
    $uploadOk = 1;
    $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

    // Controlla se il file è un'immagine
    if(isset($_POST["submit"])) {
        $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
        if($check !== false) {
            echo "File is an image - " . $check["mime"] . ".";
            $uploadOk = 1;
        } else {
            echo "File is not an image.";
            $uploadOk = 0;
        }
    }

    // Carica il file
    if ($uploadOk == 0) {
        echo "Sorry, your file was not uploaded.";
    } else {
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
            echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";

            // Estrazione dei metadati EXIF
            $exif = exif_read_data($target_file);
            if ($exif) {
                echo "<h2>Metadati Estratti:</h2>";
                echo "<table border='1'>";
                foreach ($exif as $key => $value) {
                    echo "<tr><td>$key</td><td>$value</td></tr>";
                }
                echo "</table>";
            } else {
                echo "No EXIF data found for this image.";
            }
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }
}
?>

