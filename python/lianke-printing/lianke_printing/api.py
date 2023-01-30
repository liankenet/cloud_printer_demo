from lianke_printing.base import LiankePrintingBase


class LiankePrinting(LiankePrintingBase):
    def device_info(self):
        return self.get("/device/device_info", params={"deviceId": self.device_id, "deviceKey": self.device_key})

    def printer_enum(self):
        return self.get("/print/printer_enum")

    def printer_list(self, printer_type: int = 1):
        """
        获取打印机列表
        :param printer_type: 枚举值 1.USB打印机，2.网络打印机，3.USB和网络打印机
        :return:
        """
        return self.get(
            "/external_api/printer_list",
            params={"deviceId": self.device_id, "deviceKey": self.device_key, "printerType": printer_type},
        )

    def printer_params(self, printer_model: str):
        """
        获取打印机描述信息
        :param printer_model: 打印机型号
        :return:
        """
        return self.get(
            "/print/printer_params",
            params={
                "printerModel": printer_model,
            },
        )

    def add_job(self, job_files: list, device_port: int = 1, paper_size: int = 9, timeout: int = 20, **kwargs):
        """
        添加打印任务
        :param job_files: 打印文件
        :param device_port: 打印云盒USB口
        :param paper_size: 纸张大小
        :param timeout: 发送超时时间
        :return:
        """
        post_data = {
            "deviceId": self.device_id,
            "deviceKey": self.device_key,
            "devicePort": device_port,
            "dmPaperSize": paper_size,
        }
        post_data.update(kwargs)
        return self.post("/print/job", data=post_data, files=job_files, timeout=timeout)

    def job_result(self, task_id: str, device_port: int = 1):
        """
        获取任务结果
        :param task_id: 任务ID
        :param device_port: 打印云盒端口
        :return:
        """
        return self.get(
            "/print/job",
            params={
                "deviceId": self.device_id,
                "deviceKey": self.device_key,
                "devicePort": device_port,
                "task_id": task_id,
            },
        )

    def cancel_job(self, task_id: str, device_port: int = 1):
        """
        获取任务结果
        :param task_id: 任务ID
        :param device_port: 打印云盒端口
        :return:
        """
        return self.delete(
            "/print/job",
            params={
                "deviceId": self.device_id,
                "deviceKey": self.device_key,
                "devicePort": device_port,
                "task_id": task_id,
            },
        )

    def printer_status(self, usb_port: int = 1):
        """
        获取打印机状态
        :param usb_port: 打印云盒USB端口
        :return:
        """
        return self.delete(
            "/device/printer_status",
            params={"deviceId": self.device_id, "deviceKey": self.device_key, "usbPort": usb_port},
        )
