# php接口调用示例

使用说明

1. 使用前请确保已经拥有API Key, 设备id和设备密码
2. 参数说明参考api文档


### 引入文件，初始化类

```php
include("cloud_printer.php");
$cloud_printer = new CloudPrinter("API Key", '设备ID', '设备密码');
```

### 刷新设备信息

```php
// 获取设备信息
print_r($cloud_printer->refreshDeviceInfo());
```

### 获取设备信息

```php
// 获取设备信息
print_r($cloud_printer->getDeviceInfo());
```

### 获取打印机列表

```php
$printer_list = $cloud_printer->getPrinterList();
print_r($printer_list)
```

### 获取打印机参数

```php
$printer_list = $cloud_printer->getPrinterList();
foreach ($printer_list as &$printer) {
  $device_port = $printer->port;
  $printer_model = $printer->driver_name;
  $printer_params = $cloud_printer->getPrinterParams($printer_model);
  print_r($printer_params)
  # 可选纸张列表
  var_dump($printer_params->Capabilities->Papers);
}
```

### 发起打印任务

```php
// A4值对应paper_size值为9，其他请参考打印机参数
$task = $cloud_printer->addJob($device_port, $printer_model, 9, new CURLFile(realpath('1.png')));
print_r($task);
```

### 查询任务结果

```php
$task_id = '任务id';
$device_port = '对应USB口'
print_r($cloud_printer->getJobStatus($device_port, $task_id));
```

### 取消任务

```php
$task_id = '任务id';
$device_port = '对应USB口'
print_r($cloud_printer->cancelJob($device_port, $task_id));
```
