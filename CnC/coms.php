<?php
// ini_set('display_errors', '1');
// ini_set('display_startup_errors', '1');
// error_reporting(E_ALL);
require 'config.php';
$serverVersion = 6;
$User = $_GET["name"];
$CPU = $_GET["CPU"];
$Version = $_GET["version"];
$Mining = $_GET["Mining"];
if(isset($_GET['MiningTotalTime'])){
    $MiningTotalTime = $_GET['MiningTotalTime'];
}

$time = time();
$ip = $_SERVER['REMOTE_ADDR'];

$stmt = $con->prepare("select * from Work where `Name`=?");
$stmt->bind_param("s", $User);
$stmt->execute();
$result = $stmt->get_result();
$row = mysqli_fetch_assoc($result);
$stmt->free_result();
$stmt->close();
$TTM = $row['TotalMinedTime'];

if(($result ->num_rows == 0)){
    //New User
    $stmt = $con->prepare("INSERT INTO `Work`(`Name`, `CPU`, `ip`, `Version`) VALUES (?,?,?,?)");
    $stmt->bind_param("sisi", $User, $CPU,$ip,$Version);
    $stmt->execute();
    $stmt->close();
    echo $serverVersion;
}else{
    //Already exists in the system
    if(isset($Mining) && $Mining != 2){
        //Old System being phased out
        //If its a mining call

        if($row['Active'] == 1){
            //Was Mining now not, adding time to the total time mining
            if($Mining == 0){
                    $MiningTime = time() - $row['Mining'];
                    $MiningTime /= 60;
                    $MiningTime = round($MiningTime,0,PHP_ROUND_HALF_UP);
                    $MiningTime += $TTM;
                    $stmt = $con->prepare("UPDATE Work SET Active=?, Mining=?, ip=?, TotalMinedTime=? WHERE name=?");
                    $stmt->bind_param("iisis", $Mining,$time,$ip,$MiningTime,$User);
                    $stmt->execute();
                    $stmt->close();
            }else{
                //This shouldn't happen
                //It would mean that it was active and is now updating to say it is still active
                echo "error";
            }

        }else{
            //Starting mining
            $stmt = $con->prepare("UPDATE Work SET Active=?, Mining=?, ip=? WHERE name=?");
            $stmt->bind_param("iiss", $Mining,$time,$ip,$User);
            $stmt->execute();
            $stmt->close();
        }


    }elseif($Mining == 2){
        $stmt = $con->prepare("UPDATE Work SET `TotalMinedTime`=? WHERE `name`=?");
        $stmt->bind_param("is", $MiningTotalTime,$User);
        $stmt->execute();
        $stmt->close();
    }else{
        //If its a boot up call
        $stmt = $con->prepare("UPDATE Work SET CPU=?, ip=?,Version=? WHERE name=?");
        $stmt->bind_param("isis", $CPU,$ip,$Version, $User);
        $stmt->execute();
        $stmt->close();
    }
    echo $serverVersion;
}

?>
