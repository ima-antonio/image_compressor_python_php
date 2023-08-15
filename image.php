function processImage($base64Image) {
    try {
        // Decodificar a imagem em base64
        $imageData = base64_decode($base64Image);

        // Criar uma imagem a partir dos dados decodificados
        $image = imagecreatefromstring($imageData);

        // Definir a largura desejada e calcular a altura correspondente
        $newWidth = 600;
        $aspectRatio = imagesx($image) / imagesy($image);
        $newHeight = (int) ($newWidth / $aspectRatio);

        // Redimensionar a imagem
        $resizedImage = imagecreatetruecolor($newWidth, $newHeight);
        imagecopyresampled($resizedImage, $image, 0, 0, 0, 0, $newWidth, $newHeight, imagesx($image), imagesy($image));

        // Salvar a nova imagem em um buffer
        ob_start();
        imagejpeg($resizedImage, NULL, 85);
        $compressedImageData = ob_get_clean();

        // Codificar a nova imagem em base64
        $newImageBase64 = base64_encode($compressedImageData);

        // Liberar a memória da imagem criada
        imagedestroy($image);
        imagedestroy($resizedImage);

        return $newImageBase64;
    } catch (Exception $e) {
        return ['error' => $e->getMessage()];
    }
}
