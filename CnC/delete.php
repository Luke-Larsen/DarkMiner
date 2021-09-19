<?php
session_start();

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
require 'config.php';

if(isset($_SESSION['USER'])){
    $id = $_GET['id'];
    $stmt = $con->prepare("DELETE FROM `Work` WHERE `id`=?");
    $stmt->bind_param('i', $id);
    $stmt->execute();
}

header('location:UI.php');