<?php
session_start();

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
require 'config.php';

if(isset($_SESSION['USER'])){
    echo "Coming soon <a href='UI.php'>back</a>";
}

//header('location:UI.php');