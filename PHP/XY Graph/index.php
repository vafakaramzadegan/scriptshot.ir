<?php

// Tutorial Video available on: https://www.aparat.com/v/8QKu1

$width = 600;
$height = 600;

$minX = -5;
$maxX = 5;
$minY = -5;
$maxY = 5;

$graph = imagecreatetruecolor($width, $height);

$backgroundColor = imagecolorallocate($graph, 255, 255, 255);
$gridColor = imagecolorallocate($graph, 200, 200, 200);
$axisColor = imagecolorallocate($graph, 30, 30, 30);
$equationColor = imagecolorallocate($graph, 255, 20, 20);

imagefilledrectangle($graph, 0, 0, $width, $height, $backgroundColor);

$x_count = abs($maxX - $minX);
$y_count = abs($maxY - $minY);

$pixels_in_x = $width / $x_count;
$pixels_in_y = $height / $y_count;

for ($i = 1; $i<= $y_count - 1; $i++){
    imageline($graph, 0, $i * $pixels_in_y, $width - 1, $i * $pixels_in_y, $gridColor);
}

for ($i = 1; $i<= $x_count - 1; $i++){
    imageline($graph, $i * $pixels_in_x, 0, $i * $pixels_in_x, $height - 1, $gridColor);
}

$centerYpx = ($minY >= 0 ? $height + ($minY * $pixels_in_y) : $maxY * $pixels_in_y);
$centerXpx = ($minX >= 0 ? $width + ($minX * $pixels_in_x) : $width - $maxX * $pixels_in_x);

imageline($graph, 0, $centerYpx, $width, $centerYpx, $axisColor);

imageline($graph, $centerXpx, 0, $centerXpx, $height, $axisColor);

function solve($expr, $x){
    $pattern = "/(?:[0-9-+\/,*()x]|([0-9]*[.]?)+[0-9]|\s|pi|abs|ceil|log|log10|min|rand|max|floor|ln|pow|exp|a?(?:sin|cos|tan)h?)+/i";
    if (preg_replace($pattern, "", $expr) != ""){
        return 0;
    }
    $eq = str_replace("x", $x, $expr);
    return eval("return $eq;");
}

$equation = "x";

$x = $minX;
$lastY = $centerYpx - solve($equation, $x) * $pixels_in_y;

imagesetthickness($graph, 2);

for ($i = 0; $i <= $width; $i++){
    $x += 1 / $pixels_in_x;
    $y = $centerYpx - solve($equation, $x) * $pixels_in_y;
    imageline( $graph, $i - 1, $lastY, $i, $y, $equationColor);
    $lastY = $y;
}

header("Content-Type: image/jpeg");
imagejpeg($graph, NULL, 100);
