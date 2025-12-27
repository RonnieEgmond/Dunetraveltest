<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 1. Gegevens ophalen uit het formulier
    $from    = filter_var($_POST['from'], FILTER_SANITIZE_EMAIL);
    $to      = filter_var($_POST['to'], FILTER_SANITIZE_EMAIL);
    $subject = htmlspecialchars($_POST['subject']);
    $message = htmlspecialchars($_POST['message']);
    
    // 2. Unieke scheidingslijn maken voor de bijlage (boundary)
    $boundary = md5(time());

    // 3. Headers opstellen
    $headers = "From: $from\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: multipart/mixed; boundary=\"$boundary\"\r\n";

    // 4. Het tekstgedeelte van de mail maken
    $body = "--$boundary\r\n";
    $body .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $body .= "Content-Transfer-Encoding: 7bit\r\n\r\n";
    $body .= $message . "\r\n";

    // 5. Bijlage verwerken (indien aanwezig)
    if (isset($_FILES['attachment']) && $_FILES['attachment']['error'] == UPLOAD_ERR_OK) {
        $file_name = $_FILES['attachment']['name'];
        $file_size = $_FILES['attachment']['size'];
        $file_tmp  = $_FILES['attachment']['tmp_name'];
        $file_type = $_FILES['attachment']['type'];

        // Bestand inlezen en coderen
        $handle = fopen($file_tmp, "r");
        $content = fread($handle, $file_size);
        fclose($handle);
        $encoded_content = chunk_split(base64_encode($content));

        $body .= "--$boundary\r\n";
        $body .= "Content-Type: $file_type; name=\"$file_name\"\r\n";
        $body .= "Content-Disposition: attachment; filename=\"$file_name\"\r\n";
        $body .= "Content-Transfer-Encoding: base64\r\n\r\n";
        $body .= $encoded_content . "\r\n";
    }

    $body .= "--$boundary--";

    // 6. De mail daadwerkelijk verzenden
    if (mail($to, $subject, $body, $headers)) {
        echo "<h1>Bedankt! De e-mail is succesvol verzonden.</h1>";
        echo "<a href='https://dunetraveltest.vercel.app'>Terug naar de website</a>";
    } else {
        echo "Er is helaas iets misgegaan bij het verzenden.";
    }
} else {
    echo "Geen toegang tot dit script.";
}
?>