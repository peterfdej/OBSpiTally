<!DOCTYPE html>
<?php
if(isset($_POST['save'])) 
{
	$data=simplexml_load_file('/home/pi/tally.xml');
	$data->host=$_POST['host'];
	$data->port=$_POST['port'];
	$data->pass=$_POST['pass'];
	$data->scene=$_POST['scene'];
	$handle=fopen("/home/pi/tally.xml","wb");
	fwrite($handle,$data->asXML());
	fclose($handle);
}

$data=simplexml_load_file('/home/pi/tally.xml');
$host=$data->host;
$port=$data->port;
$pass=$data->pass;
$scene=$data->scene;

?>
<head>
<style type='text/css'>
/* form elements */
label {
    display: block;
    float: left;
    width: 50px;
}
</style>
<title>Tally <?php echo $scene ?></title>
</head>
<body>
<form method="post">
	<label for="host">Host:</label>
    <textarea rows="1" cols="20" name="host" ><?php echo $host ?></textarea>
    <br>
	<label for="port">Port:</label>
	<textarea rows="1" cols="20" name="port"><?php echo $port ?></textarea>
    <br>
	<label for="pass">Pass:</label>
    <textarea rows="1" cols="20" name="pass" placeholder="*********"></textarea>
    <br>
	<label for="scene">Scene:</label>
	<textarea rows="1" cols="20" name="scene"><?php echo $scene ?></textarea>
    <br>
    <input type="submit" name="save" value="Save">
	<br><br><br>
	RED light control:
	<br>
	<input type="submit" name="on" value="ON">
	<input type="submit" name="off" value="OFF">
</form>
<?php
if(isset($_POST['on']))
{
        $gpio_on = shell_exec("/usr/local/bin/gpio -g write 24 1");
        echo "RED Light is on";
}
if(isset($_POST['off']))
{
        $gpio_off = shell_exec("/usr/local/bin/gpio -g write 24 0");
        echo "RED Light is off";
}
?>
</body>
