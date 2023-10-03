# (C) 2023 Smart Sensor Devices AB

import sys
import threading
import time
import json
import signal
import atexit

import serial.tools.list_ports

DONGLE_ARRAY = []

DUAL = "dual"
CENTRAL = "central"
PERIPHERAL = "peripheral"


class BleuIO(object):
    def __init__(self, port="auto", baud=115200, timeout=0.01, debug=False):
        """
        Initiates the dongle. If port param is left as 'auto' it will auto-detect if bleuio dongle is connected.
        :param port: str
        :param baud: int
        :param timeout: int
        :param debug: bool
        """
        self.block_time = timeout
        retry_count = 0
        self._serial = None
        self._port = None
        self.fwVersion = ""
        self._debug = debug
        self.__cmdDone = False
        self.__saveScanRsp = False
        self.__saveEvtRsp = False
        self.receiver_thread = None
        self._reader_alive = None
        self._evt_cb = None
        self._scan_cb = None
        self.gaproles = self.GapRoles()
        self.status = self.BLEStatus()
        self.__threadLock = threading.Lock()

        # Constants
        self.UUID = "UUID"
        self.CHAR_PROPERTY = "PROP"
        self.CHAR_PERMISSION = "PERM"
        self.CHAR_LENGTH = "LEN"
        self.CHAR_VALUE = "VALUE"
        self.CHAR_HEX_VALUE = "VALUEB"
        self.DESC_PERMISSION = "DPERM"
        self.DESC_LENGTH = "DLEN"
        self.DESC_VALUE = "DVALUE"
        self.DESC_HEX_VALUE = "DVALUEB"
        self.NAME = "DVALUE"
        self.MFSID = "MFSID"
        self.CLEAR = "CLEAR"

        if port == "auto":
            dongle_count = 1
            port_list = []
            while len(DONGLE_ARRAY) == 0 and retry_count < 10:
                all_ports = serial.tools.list_ports.comports(include_links=False)
                for d_port in all_ports:
                    if str(d_port.hwid).__contains__("VID:PID=2DCF"):
                        bleuio_dongle = (
                            str(dongle_count) + ") " + d_port.device + " " + d_port.hwid
                        )
                        if bleuio_dongle.__contains__("VID:PID=2DCF:6002"):
                            if self._debug:
                                print("Found dongle in port: " + d_port.device)
                            DONGLE_ARRAY.append(bleuio_dongle)
                            port_list.append(d_port)
                            dongle_count += 1
                        if bleuio_dongle.__contains__("VID:PID=2DCF:6001"):
                            if self._debug:
                                print("Bootloader in port: " + d_port.device)
                            time.sleep(2)
                            retry_count = 0
                    else:
                        pass
                retry_count += 1

            try:
                self._serial = serial.Serial(
                    port=port_list[0].device, baudrate=baud, timeout=timeout
                )
                self._port = port_list[0].device
            except (serial.SerialException, IndexError):
                raise

        else:
            if not isinstance(port, str):
                raise ValueError("Invalid port specified: {}".format(port))
            while self._serial is None:
                try:
                    self._serial = serial.Serial(
                        port=port, baudrate=baud, timeout=timeout, write_timeout=timeout
                    )
                    self._port = port
                except (ValueError, serial.SerialException) as e:
                    retry_count += 1
                    if retry_count > 3:
                        print("Error: " + str(e))
                        print("Make sure the dongle is not already in use.")
                        exit()
                    else:
                        if self._debug:
                            print(
                                "Error occurred while trying to open port. "
                                + str(e)
                                + " Retrying",
                                retry_count,
                                "/",
                                3,
                                "...",
                            )
                        time.sleep(5)

            self._serial.flushInput()
            self._serial.flushOutput()

        signal.signal(signal.SIGINT, self.__signal_handler)
        atexit.register(self.exit_handler)

        # rx task state
        self.rx_buffer = b""
        self.rx_response = []
        self.rx_scanning_results = []
        self.rx_evt_results = []

        self._start_reader()
        self.send_command("stop")
        self.send_command("ATV1")
        self.send_command("ATE1")
        self.send_command("ATI")
        # end of BleuIO.__init__()

    class BLEStatus:
        def __init__(self):
            """A class used to handle BLE Statuses

            :attr isScanning: Keeps track on if dongle is currently scanning.
            :attr isConnected: Keeps track on if dongle is currently connected.
            :attr isAdvertising: Keeps track on if dongle is currently advertising.
            :attr isSPSStreamOn: Keeps track on if dongle is currently in SPS stream mode.
            :attr role: Keeps track of the dongle's current GAP Role.
            """
            self.isScanning = False
            self.isConnected = False
            self.isAdvertising = False
            self.isSPSStreamOn = False
            self.role = ""
            # self.connectedList = []
            # self.numberOfConnections = 0

    class GapRoles:
        def __init__(self):
            """A class used to handle the different GAP Roles

            :attr PERIPHERAL:
            :attr CENTRAL:
            :attr DUAL:
            """
            self.PERIPHERAL = "peripheral"
            self.CENTRAL = "central"
            self.DUAL = "dual"

    class BleuIORESP:
        def __init__(self):
            """A class used to handle the different Dongle Responses

            :attr Cmd: Contains the command data.
            :attr Ack: Contains the acknowledge data.
            :attr Rsp: Contains list of the response data.
            :attr End: Contains the end data.
            """
            self.Cmd = None
            self.Ack = None
            self.Rsp = []
            self.End = None

    class BleuIOException(Exception):
        pass

    def __signal_handler(self, signum, frame):
        sys.exit(1)

    def __parseRspIntoJSON(self, response, careObj):
        try:
            for line in response:
                if ('{"C"') in line.decode("utf-8", "ignore"):
                    careObj.Cmd = json.loads(line)
                if ('{"A"') in line.decode("utf-8", "ignore"):
                    careObj.Ack = json.loads(line)
                if ('{"R"') in line.decode("utf-8", "ignore"):
                    careObj.Rsp.append(json.loads(line))
                if ('{"E"') in line.decode("utf-8", "ignore"):
                    careObj.End = json.loads(line)
                if ('{"SE":') in line.decode("utf-8", "ignore"):
                    careObj.Ack = json.loads(line)
        except Exception as e:
            raise self.BleuIOException(
                "Exception: " + str(e) + "\r\nError line: " + str(line) + "\r\n(Response: " + str(response) + ")"
            )
        if self._debug:
            try:
                print("debug(__parseRspIntoJSON response): " + str(response))
                print("debug(__parseRspIntoJSON line): " + str(line))
            except Exception:
                pass

    def exit_handler(self):
        self._serial.write("\x03".encode())
        self._serial.write("\x1B".encode())
        self._stop_reader()
        self._serial.close()

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        # start serial->reader thread
        self.receiver_thread = threading.Thread(target=self.__poll_serial, name="rx")
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self.receiver_thread.join()

    def __poll_serial(self):
        """Polls Dongle RX Data"""
        while self._reader_alive:
            try:
                self.rx_buffer += self._serial.read(self._serial.in_waiting)
                if self.rx_buffer and self.rx_buffer[-1:] == b'\n':
                    if str.encode('"action":"scan completed"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isScanning = False
                        self.__saveScanRsp = False
                        self.__threadLock.release()
                        if not self.__cmdDone:
                            self.__threadLock.acquire()
                            self.__cmdDone = True
                            self.rx_response.append(self.rx_buffer)
                            self.__threadLock.release()

                    if str.encode('"action":"scanning"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isScanning = True
                        self.__threadLock.release()

                    if str.encode('"action":"streaming"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isSPSStreamOn = True
                        self.__threadLock.release()

                    if str.encode('"action":"not streaming"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isSPSStreamOn = False
                        self.__threadLock.release()
                        if not self.__cmdDone:
                            self.__threadLock.acquire()
                            self.__cmdDone = True
                            self.__threadLock.release()
                            decoded_SPSStream_result = self.rx_buffer.decode(
                                "utf-8", "ignore"
                            )
                            decoded_SPSStream_resultList = []
                            decoded_SPSStream_resultList = (
                                decoded_SPSStream_result.split("\r\n")
                            )
                            for line in decoded_SPSStream_resultList:
                                if line:
                                    if ('{"R"') in line:
                                        self.rx_response.append(line.encode())

                    if str.encode('"action":"advertising stopped"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isAdvertising = False
                        self.__threadLock.release()

                    if str.encode('"action":"advertising"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isAdvertising = True
                        self.__threadLock.release()

                    if str.encode('"action":"connected"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isConnected = True
                        self.__threadLock.release()  # "action":"disconnected"

                    if str.encode('"action":"disconnected"') in self.rx_buffer:
                        self.__threadLock.acquire()
                        self.status.isConnected = False
                        self.__threadLock.release()

                    if str.encode('"evt":') in self.rx_buffer and self.__saveEvtRsp:
                        if self._evt_cb != None:
                            decoded_evt_result = self.rx_buffer.decode(
                                "utf-8", "ignore"
                            )
                            decoded_evt_resultList = []
                            decoded_evt_resultList = decoded_evt_result.split("\r\n")
                            for line in decoded_evt_resultList:
                                if line:
                                    if ('"evt":') in line:
                                        self.rx_evt_results.append(str(line))
                                        try:
                                            self.__threadLock.acquire()
                                            self._evt_cb(self.rx_evt_results)
                                            self.__threadLock.release()
                                        except:
                                            pass
                                        self.rx_evt_results = []

                    if str.encode('{"S') in self.rx_buffer and self.__saveScanRsp:
                        if self._scan_cb != None:
                            decoded_result = self.rx_buffer.decode("utf-8", "ignore")
                            decoded_resultList = []
                            decoded_resultList = decoded_result.split("\r\n")
                            for line in decoded_resultList:
                                if line:
                                    if ('{"S') in line and not ('{"SE') in line:
                                        self.rx_scanning_results.append(str(line))
                                        try:
                                            self.__threadLock.acquire()
                                            self._scan_cb(self.rx_scanning_results)
                                            self.__threadLock.release()
                                        except:
                                            pass
                                        self.rx_scanning_results = []

                    if (
                        str.encode("VERBOSE ON") in self.rx_buffer
                        and not self.__cmdDone
                    ):
                        self.__threadLock.acquire()
                        self.rx_response.append(self.rx_buffer)
                        self.__cmdDone = True
                        self.__threadLock.release()

                    if str.encode("{") in self.rx_buffer and not self.__cmdDone:
                        care_result = self.rx_buffer.decode("utf-8", "ignore")
                        care_resultList = care_result.split("\r\n")
                        for line in care_resultList:
                            changeRoleCmd = False
                            role = ""
                            if line:
                                if (
                                    ('{"C"') in line
                                    or ('{"A"') in line
                                    or ('{"R"') in line
                                    or ('{"E"') in line
                                ):
                                    if '"gap_role"' in line:
                                        jsonStr = json.loads(line)
                                        self.status.role = jsonStr["gap_role"]

                                    if '"fwVer"' in line:
                                        jsonStr = json.loads(line)
                                        self.fwVersion = jsonStr["fwVer"]
                                        if len(self.fwVersion) >= 5:
                                            checkVer = self.fwVersion[0:5]
                                            checkVer = checkVer.replace(".", "")
                                            try:
                                                checkVer = int(checkVer)
                                            except:
                                                raise self.BleuIOException(
                                                    "Cannot read firmware version!"
                                                )
                                            if checkVer < 221:
                                                raise self.BleuIOException(
                                                    "BleuIO firmware version is not supported by the BleuIO Python Library!\nSupported version is >= 2.2.1."
                                                )

                                    if '"connected"' in line and not '"action"' in line:
                                        jsonStr = json.loads(line)
                                        self.__threadLock.acquire()
                                        self.status.isConnected = jsonStr["connected"]
                                        self.__threadLock.release()

                                    if (
                                        '"advertising"' in line
                                        and not '"action"' in line
                                    ):
                                        jsonStr = json.loads(line)
                                        self.__threadLock.acquire()
                                        self.status.isAdvertising = jsonStr[
                                            "advertising"
                                        ]
                                        self.__threadLock.release()

                                    if not changeRoleCmd and "AT+PERIPHERAL" in line:
                                        changeRoleCmd = True
                                        role = PERIPHERAL
                                    if not changeRoleCmd and "AT+DUAL" in line:
                                        changeRoleCmd = True
                                        role = DUAL
                                    if not changeRoleCmd and "AT+CENTRAL" in line:
                                        changeRoleCmd = True
                                        role = CENTRAL
                                    if changeRoleCmd and '"err":0,"' in line:
                                        self.__threadLock.acquire()
                                        self.status.role = role
                                        self.__threadLock.release()
                                    self.__threadLock.acquire()
                                    self.rx_response.append(line.encode())
                                    self.__threadLock.release()
                        if b'{"E":' in self.rx_buffer:
                            self.__threadLock.acquire()
                            self.__cmdDone = True
                            self.__threadLock.release()
                    if self._debug:
                        try:
                            print("debug(rx_buffer): " + str(self.rx_buffer))
                        except Exception:
                            pass
                    self.rx_buffer = b''
            except serial.SerialException as e:
                print("exception: " + str(e))
                self.alive = False
                sys.exit(1)

    def register_scan_cb(self, callback):
        """Registers callback function for recieving scan results.

        :param callback: Function with a data parameter. Function will be called for every scan result.
        :type callback : hex str
        :returns: Scan results.
        :rtype: str
        """
        self._scan_cb = callback

    def register_evt_cb(self, callback):
        """Registers callback function for recieving events.

        :param callback: Function with a data parameter. Function will be called for every event.
        :type callback : hex str
        :returns: Event results.
        :rtype: str
        """
        self.__saveEvtRsp = True
        self._evt_cb = callback

    def unregister_scan_cb(self):
        """Unregister the callback function for recieving scan results."""
        self._scan_cb = None

    def unregister_evt_cb(self):
        """Unregister the callback function for recieving events."""
        self.__saveEvtRsp = False
        self._evt_cb = None

    def send_command(self, cmd):
        if self.status.isSPSStreamOn and cmd != "esc":
            self._serial.write(cmd.encode())
            self.rx_response.append(str('{"A":"","err": 0, "status": "ok"}').encode())
            return self.rx_response
        else:
            if self._debug:
                print("send_command: " + cmd)
            self.rx_response = []
            self._serial.reset_output_buffer()
            if self.status.isScanning and cmd != "stop":
                self.rx_response.append(
                    str(
                        '{"A":"","err": 1, "status": "Cannot send any commands while scanning."}'
                    ).encode()
                )
                self.cmd = ""
                return self.rx_response
            self.__cmdDone = False
            if cmd.__eq__("stop"):
                if self.status.isScanning:
                    self._serial.write("\x03".encode())
                    self.cmd = ""
                    while not self.__cmdDone:
                        pass
                    return self.rx_response
                else:
                    self._serial.write("\x03".encode())
                    self.cmd = ""
                    self.__cmdDone = True
                    self.rx_response.append(
                        str('{"A":"","err": 1, "status": "Not Scanning."}').encode()
                    )
                    return self.rx_response

            elif cmd.__eq__("esc"):
                if self.status.isSPSStreamOn:
                    self._serial.write("\x1B".encode())
                    self.cmd = ""
                    while not self.__cmdDone:
                        pass
                    return self.rx_response
                else:
                    self._serial.write("\x1B".encode())
                    self.cmd = ""
                    self.__cmdDone = True
                    self.rx_response.append(
                        str('{"A":"","err": 1, "status": "Not Streaming."}').encode()
                    )
                    return self.rx_response
            else:
                if not cmd == "":
                    self._serial.write(cmd.encode())
                    self._serial.write(str.encode("\r"))
                    self.cmd = ""
            while not self.__cmdDone:
                pass
            return self.rx_response

    def __at(self):
        return self.send_command("AT")

    def __ata(self, isOn):

        if isOn:
            return self.send_command("ATA1")
        if not isOn:
            return self.send_command("ATA0")

    def __atasps(self, isOn):

        if isOn:
            return self.send_command("ATASPS1")
        if not isOn:
            return self.send_command("ATASPS0")

    def __atds(self, isOn):

        if isOn:
            return self.send_command("ATDS1")
        if not isOn:
            return self.send_command("ATDS0")

    def __ate(self, isOn):

        if isOn:
            return self.send_command("ATE1")
        if not isOn:
            return self.send_command("ATE0")

    def __ati(self):
        return self.send_command("ATI")

    def __atr(self):
        return self.send_command("ATR")

    def __at_advdata(self, advData):

        if not advData == "":
            return self.send_command("AT+ADVDATA=" + advData)
        elif advData == "":
            return self.send_command("AT+ADVDATA")

    def __at_advdatai(self, advData):

        return self.send_command("AT+ADVDATAI=" + advData)

    def __at_advstart(self, conn_type, intv_min, intv_max, timer):

        if not (conn_type == "" and intv_min == "" and intv_max == "" and timer == ""):
            return self.send_command(
                "AT+ADVSTART="
                + str(conn_type)
                + ";"
                + str(intv_min)
                + ";"
                + str(intv_max)
                + ";"
                + str(timer)
                + ";"
            )
        else:
            return self.send_command("AT+ADVSTART")

    def __at_advstop(self):

        return self.send_command("AT+ADVSTOP")

    def __at_advresp(self, respData):

        if respData == "":
            return self.send_command("AT+ADVRESP")
        else:
            return self.send_command("AT+ADVRESP=" + respData)

    def __at_cancel_connect(self):

        return self.send_command("AT+CANCELCONNECT")

    def __at_central(self):

        return self.send_command("AT+CENTRAL")

    def __at_clearnoti(self, handle):

        return self.send_command("AT+CLEARNOTI=" + handle)

    def __at_clearindi(self, handle):

        return self.send_command("AT+CLEARINDI=" + handle)

    def __at_client(self):

        return self.send_command("AT+CLIENT")

    def __at_devicename(self, name):

        if name == "":
            return self.send_command("AT+DEVICENAME")
        else:
            return self.send_command("AT+DEVICENAME=" + name)

    def __at_dis(self):

        return self.send_command("AT+DIS")

    def __at_dual(self):

        return self.send_command("AT+DUAL")

    def __at_enter_passkey(self, passkey):

        return self.send_command("AT+ENTERPASSKEY=" + passkey)

    def __at_findscandata(self, scandata, timeout=0):

        self.rx_scanning_results = []
        if timeout == 0:
            return self.send_command("AT+FINDSCANDATA=" + scandata)
        else:
            return self.send_command("AT+FINDSCANDATA=" + scandata + "=" + str(timeout))

    def __at_frssi(self, rssi):

        return self.send_command("AT+FRSSI=" + rssi)

    def __at_gapaddrtype(self, addr_type):

        if addr_type == "":
            return self.send_command("AT+GAPADDRTYPE")
        else:
            return self.send_command("AT+GAPADDRTYPE=" + str(addr_type))

    def __at_gapconnect(self, addr, intv_min, intv_max, slave_latency, sup_timeout):

        adv_params = False
        if intv_min:
            if intv_max:
                if slave_latency:
                    if sup_timeout:
                        adv_params = True
                        return self.send_command(
                            "AT+GAPCONNECT="
                            + addr
                            + "="
                            + intv_min
                            + ":"
                            + intv_max
                            + ":"
                            + slave_latency
                            + ":"
                            + sup_timeout
                            + ":"
                        )
        if not adv_params:
            return self.send_command("AT+GAPCONNECT=" + addr)

    def __at_gapdisconnect(self):

        return self.send_command("AT+GAPDISCONNECT")

    def __at_gapdisconnectall(self):

        return self.send_command("AT+GAPDISCONNECTALL")

    def __at_gapiocap(self, io_cap):

        if io_cap == "":
            return self.send_command("AT+GAPIOCAP")
        else:
            return self.send_command("AT+GAPIOCAP=" + io_cap)

    def __at_gappair(self, bond):

        if bond:
            return self.send_command("AT+GAPPAIR=BOND")
        else:
            return self.send_command("AT+GAPPAIR")

    def __at_gapscan(self, timeout):

        self.rx_scanning_results = []
        if not timeout == 0:
            return self.send_command("AT+GAPSCAN=" + str(timeout))
        if timeout == 0:
            return self.send_command("AT+GAPSCAN")

    def __at_gapunpair(self, addr):

        if addr == "":
            return self.send_command("AT+GAPUNPAIR")
        else:
            return self.send_command("AT+GAPUNPAIR=" + addr)

    def __at_gapstatus(self):

        return self.send_command("AT+GAPSTATUS")

    def __at_gattcread(self, uuid):

        return self.send_command("AT+GATTCREAD=" + uuid)

    def __at_gattcwrite(self, uuid, data):

        return self.send_command("AT+GATTCWRITE=" + uuid + " " + data)

    def __at_gattcwriteb(self, uuid, data):

        return self.send_command("AT+GATTCWRITEB=" + uuid + " " + data)

    def __at_gattcwritewr(self, uuid, data):

        return self.send_command("AT+GATTCWRITEWR=" + uuid + " " + data)

    def __at_gattcwritewrb(self, uuid, data):

        return self.send_command("AT+GATTCWRITEWRB=" + uuid + " " + data)

    def __at_get_services(self):

        return self.send_command("AT+GETSERVICES")

    def __at_get_services_only(self):

        return self.send_command("AT+GETSERVICESONLY")

    def __at_get_service_details(self, uuid):

        return self.send_command("AT+GETSERVICEDETAILS=" + uuid)

    def __at_get_conn(self):

        return self.send_command("AT+GETCONN")

    def __at_get_mac(self):

        return self.send_command("AT+GETMAC")

    def __at_indi(self):

        return self.send_command("AT+INDI")

    def __at_noti(self):

        return self.send_command("AT+NOTI")

    def __at_numcompa(self, auto_accept):

        if auto_accept == "0":
            return self.send_command("AT+NUMCOMPA=0")
        elif auto_accept == "1":
            return self.send_command("AT+NUMCOMPA=1")
        elif auto_accept == "2":
            return self.send_command("AT+NUMCOMPA")

    def __at_peripheral(self):

        return self.send_command("AT+PERIPHERAL")

    def __at_scantarget(self, addr):

        return self.send_command("AT+SCANTARGET=" + addr)

    def __at_sec_lvl(self, sec_lvl):

        if sec_lvl == "":
            return self.send_command("AT+SECLVL")
        else:
            return self.send_command("AT+SECLVL=" + sec_lvl)

    def __at_server(self):

        return self.send_command("AT+SERVER")

    def __at_set_dis(self, manuf, model_num, serial_num, hw_rev, fw_rev, sw_rev):

        return self.send_command(
            "AT+SETDIS="
            + manuf
            + "="
            + model_num
            + "="
            + serial_num
            + "="
            + hw_rev
            + "="
            + fw_rev
            + "="
            + sw_rev
        )

    def __at_set_noti(self, handle):

        return self.send_command("AT+SETNOTI=" + handle)

    def __at_set_indi(self, handle):

        return self.send_command("AT+SETINDI=" + handle)

    def __at_set_passkey(self, passkey):

        if passkey == "":
            return self.send_command("AT+SETPASSKEY")
        else:
            return self.send_command("AT+SETPASSKEY=" + passkey)

    def __at_show_rssi(self, rssi):

        if rssi:
            return self.send_command("AT+SHOWRSSI=1")
        else:
            return self.send_command("AT+SHOWRSSI=0")

    def __at_spssend(self, data=""):

        if not self.status.isSPSStreamOn:
            if data == "":
                return self.send_command("AT+SPSSEND")
            if not data == "":
                return self.send_command("AT+SPSSEND=" + data)
        else:
            return self.send_command(data)

    def __at_target_conn(self, conn_idx):

        if conn_idx == "":
            return self.send_command("AT+TARGETCONN")
        else:
            return self.send_command("AT+TARGETCONN=" + conn_idx)

    def __at_scanfilter(self, sftype, value):
        if sftype == None and value == "":
            return self.send_command("AT+SCANFILTER")
        else:
            if value == "":
                return self.send_command("AT+SCANFILTER=" + str(sftype))
            else:
                return self.send_command("AT+SCANFILTER=" + str(sftype) + "=" + value)

    def __at_customservice(self, idx, cstype, value):
        if idx == None and cstype == None and value == "":
            return self.send_command("AT+CUSTOMSERVICE")
        else:
            return self.send_command(
                "AT+CUSTOMSERVICE=" + str(idx) + "=" + str(cstype) + "=" + value
            )

    def __at_customservice_start(self):
        return self.send_command("AT+CUSTOMSERVICESTART")

    def __at_customservice_stop(self):
        return self.send_command("AT+CUSTOMSERVICESTOP")

    def __at_customservice_reset(self):
        return self.send_command("AT+CUSTOMSERVICERESET")
    
    def __at_suota_start(self):
        return self.send_command("AT+SUOTASTART")

    def __at_suota_stop(self):
        return self.send_command("AT+SUOTASTOP")        

    def __help(self):

        return self.send_command("--H")

    def __stop_scan(self):

        return self.send_command("stop")

    def __stop_sps(self):

        return self.send_command("esc")

    def stop_scan(self):
        """Stops any type of scan.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__stop_scan()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def stop_sps(self):
        """Stops SPS Stream-mode.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__stop_sps()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at(self):
        """Basic AT-Command.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def ata(self, isOn):
        """Shows/hides ascii values from notification/indication/read responses.

        :param isOn: True=On, False=Off
        :type isOn : bool
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__ata(isOn)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def atasps(self, isOn):
        """Toggle between ascii (Off) and hex responses (On) received from SPS.

        :param isOn: True=On, False=Off
        :type isOn : bool
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__atasps(isOn)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def atds(self, isOn):
        """Turns auto discovery of services when connecting on/off.

        :param isOn: (boolean) True=On, False=Off
        :type isOn : bool
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__atds(isOn)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def ate(self, isOn):
        """Turns Echo on/off.

        :param isOn: (boolean) True=On, False=Off
        :type isOn : bool
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__ate(isOn)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def ati(self):
        """Device information query.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__ati()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def atr(self):
        """Trigger platform reset.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__atr()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_advdata(self, advdata=""):
        """Sets or queries the advertising data.

        :param: Sets advertising data. If left empty it will query what advdata is set. Format: xx:xx:xx:xx:xx.. (max 31 bytes)
        :type advdata: hex str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_advdata(advdata)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_advdatai(self, advdata):
        """Sets advertising data in a way that lets it be used as an iBeacon.
        Format = (UUID)(MAJOR)(MINOR)(TX)
        Example: at_advdatai("5f2dd896-b886-4549-ae01-e41acd7a354a0203010400")

        :param: Sets advertising data in iBeacon format. If left empty it will query what advdata is set
        :type advdata: hex str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_advdatai(advdata)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_advstart(self, conn_type="", intv_min="", intv_max="", timer=""):
        """Starts advertising with default settings if no params.
        With params: Starts advertising with <conn_type><intv_min><intv_max><timer>.

        :param: Starts advertising with default settings.
        :type conn_type: str
        :type intv_min: str
        :type intv_max: str
        :type timer: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_advstart(conn_type, intv_min, intv_max, timer)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_advstop(self):
        """Stops advertising.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_advstop()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_advresp(self, respData=""):
        """Sets or queries scan response data. Data must be provided as hex string.

        :param: Sets scan response data. If left empty it will query what advdata is set. Format: xx:xx:xx:xx:xx.. (max 31 bytes)
        :type respData: hex str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_advresp(respData)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_cancel_connect(self):
        """While in Central Mode, cancels any ongoing connection attempts.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_cancel_connect()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_central(self):
        """Sets the device Bluetooth role to central role.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_central()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_clearnoti(self, handle):
        """Disables notification for selected characteristic.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_clearnoti(handle)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_clearindi(self, handle):
        """Disables indication for selected characteristic.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_clearindi(handle)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_client(self):
        """Sets the device role towards the targeted connection to client. Only in dual role.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_client()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_divicename(self, name=""):
        """Gets or sets the device name.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_devicename(name)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_dis(self):
        """Shows the DIS Service info and if the DIS info is locked in or can be changed.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_dis()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_dual(self):
        """Sets the device Bluetooth role to dual role.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_dual()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_enter_passkey(self, passkey):
        """Respond to Passkey request. When faced with this message: BLE_EVT_GAP_PASSKEY_REQUEST use this command to enter
        the 6-digit passkey to continue the pairing request.

        :param passkey: str: six-digit number string "XXXXXX"
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_enter_passkey(passkey)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_findscandata(self, scandata="", timeout=0):
        """Scans for all advertising/response data which contains the search params.

        :param scandata: Hex string to filter the advertising/scan response data. Can be left blank to scan for everything. Format XXXX..
        :type scandata: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        scandata = scandata.upper()
        care = self.__at_findscandata(scandata, timeout)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)
        self.__saveScanRsp = True
        if self._scan_cb == None:
            self.send_command("stop")
            self.__saveScanRsp = False

        return response

    def at_frssi(self, rssi):
        """Filters scan results, showing only results with <max_rssi> value or lower.

        :param rssi: RSSI value. Must be negative. eg. -67
        :type rssi: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_frssi(rssi)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapaddrtype(self, addr_type=""):
        """Change device Address Type or queries device Address Type.

        :param addr_type: Range: 1-5. If left blank queries current Address Type.
        :type addr_type: int
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapaddrtype(addr_type)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapconnect(
        self,
        addr,
        intv_min="",
        intv_max="",
        slave_latency="",
        sup_timeout="",
    ):
        """Initiates a connection with a specific slave device. [<addr_type>]<address>=<intv_min>:<intv_max>:<slave_latency>:<sup_timeout>

        :param addr: hex str format: [X]XX:XX:XX:XX:XX:XX
        :param intv_min: str
        :param intv_max: str
        :param slave_latency: str
        :param sup_timeout: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """

        care = self.__at_gapconnect(
            addr, intv_min, intv_max, slave_latency, sup_timeout
        )
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapdisconnect(self):
        """Disconnects from a peer Bluetooth device.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapdisconnect()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapdisconnectall(self):
        """Disconnects from all peer Bluetooth devices.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapdisconnectall()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapiocap(self, io_cap=""):
        """Sets or queries what input and output capabilities the device has. Parameter is number between 0 to 4.

        :param io_cap: str: number
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapiocap(io_cap)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gappair(self, bond=False):
        """Starts a pairing (bond=False) or bonding procedure (bond=True).

        :param bond: boolean
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gappair(bond)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapunpair(self, addr_to_unpair=""):
        """Unpair paired devices if no parameters else unpair specific device. This will also remove the device bond data
        from BLE storage.
        Usable both when device is connected and when not.

        :param addr_to_unpair: hex str format: [X]XX:XX:XX:XX:XX:XX
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapunpair(addr_to_unpair)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gapscan(self, timeout=0):
        """Starts a Bluetooth device scan with or without timer set in seconds.

        :param: if left empty it will scan indefinitely
        :param timeout: int (time in seconds)
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapscan(timeout)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)
        self.__saveScanRsp = True
        if self._scan_cb == None:
            self.send_command("stop")
            self.__saveScanRsp = False

        return response

    def at_gapstatus(self):
        """Reports the Bluetooth role.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gapstatus()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gattcread(self, uuid):
        """Read attribute of remote GATT server.

        :param uuid: hex str format: XXXX
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gattcread(uuid)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gattcwrite(self, uuid, data):
        """Write attribute to remote GATT server in ASCII.

        :param uuid: hex str format: XXXX
        :param data: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gattcwrite(uuid, data)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gattcwriteb(self, uuid, data):
        """Write attribute to remote GATT server in Hex.

        :param uuid: hex str format: XXXX
        :param data: hex str format: XXXXXXX..
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gattcwriteb(uuid, data)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gattcwritewr(self, uuid, data):
        """Write, without response, attribute to remote GATT server in ASCII.

        :param uuid: hex str format: XXXX
        :param data: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gattcwritewr(uuid, data)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_gattcwritewrb(self, uuid, data):
        """Write, without response, attribute to remote GATT server in Hex.

        :param uuid: hex str format: XXXX
        :param data: hex str format: XXXXXXX..
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_gattcwritewrb(uuid, data)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_get_conn(self):
        """Gets a list of currently connected devices along with their mac addresses and conn_idx.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_get_conn()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_get_mac(self):
        """Returns MAC address of the BleuIO device.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_get_mac()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_get_services(self):
        """Discovers all services of a peripheral and their descriptors and characteristics.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_get_services()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_get_servicesonly(self):
        """Discovers a peripherals services.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_get_services_only()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_get_service_details(self, uuid):
        """Discovers all characteristics and descriptors of a selected service.

        :param uuid: hex str format: XXXX
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_get_service_details(uuid)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_indi(self):
        """Show list of set indication handles.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_indi()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_noti(self):
        """Show list of set notification handles.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_noti()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_numcompa(self, auto_accept="2"):
        """Used for accepting a numeric comparison authentication request (no params) or enabling/disabling auto-accepting
        numeric comparisons. auto_accept="0" = off, auto_accept="1" = on.

        :param auto_accept: str format: "0" or "1"
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_numcompa(auto_accept)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_peripheral(self):
        """Sets the device Bluetooth role to peripheral.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_peripheral()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_scantarget(self, addr):
        """Scan a target device. Displaying it's advertising and response data as it updates.

        :param addr: hex str format: "xx:xx:xx:xx:xx:xx"
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """

        care = self.__at_scantarget(addr)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)
        self.__saveScanRsp = True
        if self._scan_cb == None:
            self.send_command("stop")
            self.__saveScanRsp = False

        return response

    def at_sec_lvl(self, sec_lvl=""):
        """Sets or queries (no params) what minimum security level will be used when connected to other devices.

        :param sec_lvl:  str: string number between 0 and 4
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_sec_lvl(sec_lvl)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_server(self):
        """Sets the device role towards the targeted connection to server. Only in dual role.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_server()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_setdis(self, manuf, model_num, serial_num, hw_rev, fw_rev, sw_rev):
        """Sets the DIS Service info.

        :param manuf: str
        :param model_num: str
        :param serial_num: str
        :param hw_rev: str
        :param fw_rev: str
        :param sw_rev: str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_set_dis(manuf, model_num, serial_num, hw_rev, fw_rev, sw_rev)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_set_noti(self, handle):
        """Enable notification for selected characteristic.

        :param handle: hex str format: "xxxx"
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_set_noti(handle)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_set_indi(self, handle):
        """Enable indication for selected characteristic.

        :param handle: hex str format: "xxxx"
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_set_indi(handle)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_set_passkey(self, passkey=""):
        """Setting or quering set passkey (no params) for passkey authentication.

        :param passkey: hex str format: "xxxxxx"
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_set_passkey(passkey)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_show_rssi(self, show_rssi=True):
        """Shows/hides RSSI in AT+FINDSCANDATA and AT+SCANTARGET scans.

        :param show_rssi: bool
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_show_rssi(show_rssi)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_spssend(self, data=""):
        """Send a message or data via the SPS profile.
        Without parameters it opens a stream for continiously sending data.

        :param: if left empty it will open Streaming mode
        :type data: str or None
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        response = self.BleuIORESP()
        care = self.__at_spssend(data)
        self.__parseRspIntoJSON(care, response)

        return response

    def at_target_conn(self, conn_idx=""):
        """Set or quering the connection index which is the targeted connection.

        :param conn_idx: connection index, format: xxxx
        :type conn_idx : hex str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_target_conn(conn_idx)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_scanfilter(self, sftype: str = None, value: str = ""):
        """Sets or queries the scanfilter. There are three types of scanfilter, filter by name, filter by uuid or by manufacturer specific ID.

        :param sftype: scan filter parameter type
        :type sftype : str
        :param value: value
        :type value : str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_scanfilter(sftype, value)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_customservice(self, idx: int = None, cstype: str = None, value: str = ""):
        """Sets or queries Custom Service. Max 5 Characteristics can be added.
            Several values cannot be changed while connected/connecting or advertising.

        :param idx: service index
        :type idx : number
        :param cstype: custom service parameter type
        :type cstype : str
        :param value: value
        :type value : str
        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_customservice(idx, cstype, value)
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_customservice_start(self):
        """Starts the Custom Service based on the settings set by AT+CUSTOMSERVICE= Command.
            Cannot be started while connected/connecting or advertising

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_customservice_start()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_customservice_stop(self):
        """Stops the Custom Service.
            Cannot be changed while connected/connecting or advertising.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_customservice_stop()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_customservice_reset(self):
        """Stops the Custom Service and resets the Custom Service settings set by the AT+CUSTOMSERVICE= command to it's default values.
            Cannot be changed while connected/connecting or advertising..

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_customservice_reset()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response
    
    def at_suota_start(self):
        """Enables the SUOTA Service and start the SUOTA Advertising.
           Cannot be started while connected/connecting or advertising.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_suota_start()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response

    def at_suota_stop(self):
        """Disables the SUOTA Service and stops the SUOTA Advertising.
           Cannot be used while connected/connecting.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects.
        :rtype: obj BleuIORESP
        """
        care = self.__at_suota_stop()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response        

    def help(self):
        """Shows all AT-Commands.

        :returns: Object with 4 object properties: Cmd, Ack, Rsp and End. Each property contains a JSON object, except for Rsp which contains a list of JSON objects. except for Rsp which contains a list of JSON objects.
        :rtype obj BleuIORESP
        """
        care = self.__help()
        response = self.BleuIORESP()
        self.__parseRspIntoJSON(care, response)

        return response
