<?php

// CODIGO PHP PARA EXECUTAR O PYTHON E ABRIR O FLASK
$comando = 'c:/xampp/htdocs/Relatorio-Vetorian/venv/Scripts/python.exe c:/xampp/htdocs/Relatorio-Vetorian/index.py';
$process = proc_open($comando, [], $pipes);
if (is_resource($process)) {
    $url = 'http://127.0.0.1:5000/relatorio';
    $formData = array(
        'placa' => 'SUZ0138',
        'data' => '2023-07-29'
    );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($formData));

    $response = curl_exec($ch);
    curl_close($ch);

    echo $response;
    sleep(7);
    proc_terminate($process);
    proc_close($process);
}
?>