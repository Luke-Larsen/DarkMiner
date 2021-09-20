<?php
session_start();

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
require 'config.php';

if(isset($_SESSION['USER'])){
    echo "
    Work in progress coming soon<br>
    <form action='' method='post'>
    <label for='versions'>Choose a version:</label>
    <select id='versions' name='versions'>
        <option value='1'>1</option>
    </select>
    </form>
    ";
}

//header('location:UI.php');