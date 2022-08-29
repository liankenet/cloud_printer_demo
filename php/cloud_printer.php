<?php

class ApiException extends Exception
{
}

class HttpException extends Exception
{
}

class CloudPrinter
{
  // 声明属性
  public $api_key = '';
  public $server = "https://cloud.wisiyilink.com/";
  public $timeout = 10;
  public $debug = false;
  public $device_id = '';
  public $device_key = '';

  public function CloudPrinter($api_key, $device_id, $device_key, $debug = false, $timeout = 10)
  {
    $this->api_key = $api_key;
    $this->timeout = $timeout;
    $this->device_id = $device_id;
    $this->device_key = $device_key;
    $this->debug = $debug;
  }

  private function requests($method, $endpoint, $fields = array(), $content_type = 'application/json')
  {
    if ($method == 'POST' && $content_type == 'application/json') {
      $fields = json_encode($fields);
    }
    $curl = curl_init();

    $headers = array(
      "ApiKey: " . $this->api_key
    );
    if ($method == "POST") {
      array_push($headers, 'Content-Type: ' . $content_type);
    }

    curl_setopt_array($curl, array(
      CURLOPT_URL => $this->server . $endpoint,
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_MAXREDIRS => 1,
      CURLOPT_TIMEOUT => $this->timeout,
      CURLOPT_FOLLOWLOCATION => true,
      CURLINFO_HEADER_OUT => $this->debug,
      CURLOPT_VERBOSE => $this->debug,
      CURLOPT_CUSTOMREQUEST => $method,
      CURLOPT_POSTFIELDS => $fields,
      CURLOPT_HTTPHEADER => $headers,
    ));

    $response = curl_exec($curl);

    $info = curl_getinfo($curl);
    if ($this->debug) {
      print_r($info);
    }

    if (false === $response) {
      die(curl_error($curl));
      throw new Exception(curl_error($curl), curl_errno($curl));
    } else if ($info['http_code'] != 200) {
      throw new HttpException(curl_error($curl), $info['http_code']);
    }
    $data = json_decode($response);
    if ($data->code != 200) {
      throw new ApiException($data->msg, $data->code);
    }
    return $data;
  }

  public function getDeviceInfo()
  /*
  * 设备信息
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
    );
    $response = $this->requests("GET", 'api/device/device_info?' . http_build_query($data));
    return $response->data;
  }

  public function asyncRefreshDeviceInfo()
  /*
  * 异步刷新设备信息，包括打印机信息
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
    );
    $response = $this->requests("GET", 'api/device/async_refresh_device_info?' . http_build_query($data));
    return $response;
  }
  
  public function getPrinterList()
  /*
  * 打印机列表
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
    );
    $response = $this->requests("GET", 'api/external_api/printer_list?' . http_build_query($data));
    return $response->data->row;
  }

  public function getPrinterParams($printer_model)
  /**
  * 打印参数
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
      "printerModel" => $printer_model,
    );
    $response = $this->requests("GET", 'api/print/printer_params?' . http_build_query($data));
    return $response->data;
  }

  public function addJob($device_port, $printer_model, $paper_size, $file, $optional_array = array())
  /*
  * 发起打印任务
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
      "devicePort" => $device_port,
      "printerModel" => $printer_model,
      "dmPaperSize" => $paper_size,
      "jobFile" => $file
    );
    $data = array_merge($data, $optional_array);
    $response = $this->requests("POST", 'api/print/job', $data, "multipart/form-data");
    return $response->data;
  }

  public function getJobStatus($device_port, $task_id)
  /*
  * 获取任务状态
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
      "devicePort" => $device_port,
      "task_id" => $task_id,
    );
    $response = $this->requests("GET", 'api/print/job?' . http_build_query($data));
    return $response->data;
  }

  public function cancelJob($device_port, $task_id)
  /*
  * 取消任务
  */
  {
    $data = array(
      "deviceId" => $this->device_id,
      "deviceKey" => $this->device_key,
      "devicePort" => $device_port,
      "task_id" => $task_id,
    );
    $response = $this->requests("DELETE", 'api/print/job?' . http_build_query($data));
    return $response;
  }
}
