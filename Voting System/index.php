<html>
<head>
<meta http-equiv="refresh" content="5">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>VOTING SYSTEM</title>
</head>
<body style="background-color:#00664d;text-align: center;">
<h1 style="color:ffffff; text-align: center;">FACE RECOGNITION & FINGER PRINT VOTING SYSTEM</h1>


<?php
/*<button onclick="myFunction()">WEBCAM SERVER</button>
<p id="demo"></p>
<script>
function myFunction() 
{
    //document.getElementById("demo").innerHTML = "Hello";
}
</script>
*/
date_default_timezone_set('Asia/Kolkata');
$date = date('d-m-y h:i:s');
echo $date;
//echo "<font size=5 color=ffffff >$dt</font>";
//echo "<br>";
//echo "<br>";

/*echo "Time is ".date("h:i:sa")."<br>";
echo "<br>";
echo "<br>";*/

//$section = file_get_contents('1.txt');
//$str_parts = preg_split("/\r\n|\r|\n/", $section);
//echo "<font size=5 color=ffffff >$str_parts[0]</font>";

$count = file_get_contents('count.txt', NULL, NULL, 0, 2);

echo '<div align="LEFT">' ."Vote Count : ";
echo "<font size=4 color=ffffff >$count</font>";
echo "<br>";
echo "<br>";

for($x = 1; $x <= $count; $x++)
{

$id = (string)$x;
//echo "<font size=5 color=ffffff >$t</font>";
//echo "<br>";
//echo "<br>";

//$section = file_get_contents($Product_Server_Path.$id.'.txt', NULL, NULL, 12, 8);
$section = file_get_contents($id.'.txt');
$str_parts = explode(";",$section);

echo "<br>";echo "<br>";
echo "<br>";echo "<br>";
echo "<font size=5</font>";
echo '<div align="LEFT">' ."PERSON NAME : ";
echo "<font size=5 color=ffffff >$str_parts[0]</font>";
echo "<br>";
echo "<br>";

echo '<div align="LEFT">' ."PERSON ID : ";
echo "<font size=5 color=ffffff >$str_parts[1]</font>";
echo "<br>";
echo "<br>";

echo '<div align="LEFT">' ."VOTE STATUS : ";

if ($str_parts[2] == 1)
{
echo "<font size=5 color=ffffff >DONE    </font>";
}
echo "<br>";
echo "<br>";

$Image_Path = $str_parts[3];

//echo "<font size=5 color=ffffff >$section</font>";
//echo "<img src ='person_update/img1.jpg' style='float:left;margin-left:1%;' id='oop' width='200' height='200'>" ;
echo "<img src ='$Image_Path' style='float:left;margin-left:1%;' id='oop' width='300' height='240'>" ;
//echo ' <img src="img1.jpg" /> ' ;

echo "<br>";echo "<br>";
echo "<br>";
echo "<br>";echo "<br>";
echo "<br>";echo "<br>";
echo "<br>";echo "<br>";
echo "<br>";echo "<br>";
echo "<br>";


}

?>
</body>
</html>
