<?php
session_start();

//UPDATE: Create a lock down mode that will 404 anyone who doesn't have a cookie or php session

ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);
require 'config.php';

function secondsToTime($ss) {
    $s = $ss%60;
    $m = floor(($ss%3600)/60);
    $h = floor(($ss%86400)/3600);
    $d = floor(($ss%2592000)/86400);
    $M = floor($ss/2592000);
    if($M > 0){
        return "$M months, $d days, $h hours, $m minutes, $s seconds";
    }elseif($d >0){
        return "$d days, $h hours, $m minutes, $s seconds";
    }elseif($h > 0){
        return "$h hours, $m minutes, $s seconds";
    }elseif($m > 0){
        return "$m minutes, $s seconds";
    }elseif($s > 0){
        return "$s seconds";
    }
}

//Get domain server is hosted on
$actual_link = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

$stmt = $con->prepare("select * from config");
$stmt->execute();
$result = $stmt->get_result();
while($row = mysqli_fetch_assoc($result)){
    if($row['Name'] == "Password"){
        $hashPassword = $row['Value'];
    }
}

if(isset($_POST['passwordChangeFormSubmit'])){
    $userSuppliedPassword = $_POST['password'];
    $userSuppliedPasswordConf = $_POST['password1'];
    if($userSuppliedPassword == $userSuppliedPasswordConf){
        if($hashPassword == "MySecurePassword"){
            $ChangePassword = password_hash($userSuppliedPassword,PASSWORD_DEFAULT);
            $dbDataName = 'Password';
            $stmt = $con->prepare("UPDATE `config` SET `Value`=? WHERE `Name`=?");
            $stmt->bind_param('ss',$ChangePassword,$dbDataName);
            $stmt->execute();
        }
    }
}
?>
<html>
    <head>
        <script src='https://www.google.com/recaptcha/api.js'></script>
        <link href="assets/css/style.css" rel="stylesheet" type="text/css" media="all">
    </head>
    <body>
        <?php
        if(isset($_GET['logout'])){
            unset($_SESSION["USER"]);
            session_regenerate_id();
            session_unset();
            session_destroy();
            session_write_close();
            setcookie(session_name(),'',0,'/');
            $actual_link = str_replace( "?logout=1", "", $actual_link );
            echo "
            Logged out. 
            <a href='$actual_link'>Click here if not redirected</a>
            <script>location.href = '$actual_link';</script>
            ";
        }

        if(isset($_POST['passwordFormSubmit'])){
            $userSuppliedPassword = $_POST['password'];
            $captcha = $_POST['g-recaptcha-response'];
            $rsp  = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=$googleCaptchaSecret&response=$captcha");
            $arr = json_decode($rsp,TRUE);
            if($arr['success']){
                if($hashPassword == "MySecurePassword" && $userSuppliedPassword == $hashPassword){
                    exit("
                    Please change your password:
                    <form action='' name='passwordChangeForm' method='post'>
                        Password : <input name='password' type='text'>
                        Confirm Password : <input name='password1' type='text'>
                        <input name='passwordChangeFormSubmit' type='submit' value='Submit'>
                    </form>
                    ");
                }else{
                    if (password_verify($userSuppliedPassword, $hashPassword)){
                        session_regenerate_id();
                        //UPDATE: to set the session with a secure key and cookie to keep user logged in
                        $_SESSION["USER"] = 'User';
                        echo "Success     
                        <a href='$actual_link'>Click here if not redirected</a>
                        <script>location.href = '$actual_link';</script>";
                    }else{
                        echo "wrong password";
                    }
                }
            }else{
                echo "Bad captcha";
            }

        }else{
            //Stop user if they aren't proven to be authorized
            if(!isset($_SESSION['USER'])){
                echo "
                    <form action='' name='passwordForm' method='post'>
                        Password : <input name='password' type='password'>
                        <input name='passwordFormSubmit' type='submit' value='Submit'>
                        <div class='g-recaptcha' data-sitekey='$googleCaptchaPublic'></div>
                    </form>";
            }else{
                //page stuff
                echo "<a href='?logout=1'>logout</a><br>";
                echo "<a href=settings.php>Settings</a>";
                //Data about computers
                $stmt = $con->prepare("select * from Work");
                $stmt->execute();
                $result = $stmt->get_result();
                echo "<h2>Computers</h2>";
                echo "
                <table style='width:100%'>
                    <tr>
                        <th>Name</th>
                        <th>Total Idle Time</th>
                        <th>Last Seen</th>
                        <th>Controls</th>
                    </tr>        
                ";
                while($row = mysqli_fetch_assoc($result)){
                    $Computer = $row['Name'];
                    $Active = $row['Active'];
                    $TotalMinedTime = $row['TotalMinedTime'];
                    $lastSeen = $row['lastSeen'];
                    $id = $row['id'];
                    $TotalMinedTimeHumanReadable = secondsToTime($TotalMinedTime);
                    if($Active){
                        echo "
                            <tr>
                                <td style='color:green'>$Computer</td>
                                <td>$TotalMinedTimeHumanReadable</td> 
                                <td>$lastSeen</td>
                                <td><a href='delete.php?id=$id'>delete</a></td>
                            </tr>
                            ";
                    }else{
                        echo "
                            <tr>
                                <td style='color:red'>$Computer</td>
                                <td>$TotalMinedTimeHumanReadable</td> 
                                <td>$lastSeen</td>
                                <td><a href='delete.php?id=$id'>delete</a></td>
                            </tr>
                        ";
                    }
                    
                }
            }
        }
        ?>
    </body>
</html>