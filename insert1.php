<html>
<head>
<meta charset="UTF-8" />
<title>DHT</title>
<meta http-equiv="refresh" content="3;url=http://127.0.0.1/insert.php">
</head>
<body>
<?php
// 發送HTTP請求並返回JSON
function httpRequest($api, $data_string) {
    $ch = curl_init($api);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'Content-Length:' . strlen($data_string))
    );
    
    $result = curl_exec($ch);
    curl_close($ch);
    return json_decode($result, true);
}

// 創建包含溫度和濕度數據的數組
$data = array(
    "d" => $_GET["d"]
);

// 發送HTTP POST請求執行上傳動作
$data = httpRequest('http://127.0.0.1:8000/G001/', json_encode($data));

// 發送HTTP POST請求執行讀取動作
$data = httpRequest('http://127.0.0.1:8000/G002/', json_encode($data));

// 將返回的數據顯示於Html
foreach ($data as $value){
    echo "ID:".$value['Id']."<br>";
    echo "Celisius:".$value['Celisius']."<br>";
    echo "Fahrenheit:".$value['Fahrenheit']."<br>";
    echo "Humidity:".$value['Humidity']."<br>";
}
?>
</body>
</html>