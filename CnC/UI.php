<?php
session_start();
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);
require 'config.php';

//UPDATE:Change this to be part of the mysql also make it impossible to use default password
$password = 'MySecurePassword';

$hashPassword = password_hash($password,PASSWORD_DEFAULT);

if(isset($_POST['passwordFormSubmit'])){
    $userSuppliedPassword = $_POST['password'];
    if (password_verify($userSuppliedPassword, $hashPassword)){
        session_regenerate_id();
        //UPDATE: to set the session with a secure key and cookie to keep user logged in
        $_SESSION["USER"] = 'User';
    }else{
        echo "wrong password";
    }
}
//Stop user if they aren't proven to be authorized
if(!isset($_SESSION['USER'])){
    echo "<form action='' name='passwordForm' method='post'>Password : <input name='password' type='text'><input name='passwordFormSubmit' type='submit' value='Submit'></form>";
}else{
    $stmt = $con->prepare("select * from Work");
    $stmt->execute();
    $result = $stmt->get_result();
    while($row = mysqli_fetch_assoc($result)){
        $Computer = $row['Name'];
        $Active = $row['Active'];
        $TotalMinedTime = $row['TotalMinedTime'];
        echo "$Computer : $Active : $TotalMinedTime <br>";
    }
}
?>