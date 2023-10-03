import os, sys, time, subprocess, mystring
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from vbox_extra.gen import VirtualBox,ExtraDataItem,Snapshot,StorageController,AttachedDevice,Image,Snapshots,HardDisk

if False:
    def add_snapshot(self:VirtualBox, snapshot_path:str, snapshot_folder:str):
        """
        VDI located in StorageControllers-attachedDevice-Image (uuid):> {06509f60-d51f-4ce4-97ed-f83cff79d93e}
        Also located in Machine -> MediaRegistry -> HardDisks -> HardDisk
        """
        import uuid, datetime
        from copy import deepcopy as dc

        copy_hardware = dc(self.machine.hardware)

        # Fix the VMDK Potential
        save_files, vdi_file = [], None
        vmdk_files = []
        for filename in os.scandir(snapshot_folder):
            if os.path.isfile(filename.path):
                if filename.name.endswith('.sav'):
                    save_files += [filename.path]
                if filename.name.endswith('.vdi'):
                    vdi_file = filename.path
                if filename.name.endswith('.vmdk'):
                    vmdk_files += [filename.path]
            print(filename.name)
        print(vdi_file)
        save_files.sort(key=lambda date: datetime.datetime.strptime(
            '-'.join(date.replace('Snapshots/', '').replace('.sav', '').split("-")[:-1]), "%Y-%m-%dT%H-%M-%S"))

        last_snapshot = self.machine.snapshot.uuid

        ini_snapshot = Snapshot(
            uuid="{" + str(uuid.uuid4()) + "}",
            name="SnapShot := 0",
            # time_stamp=save_file_date,
            # state_file=X,
            hardware=dc(self.machine.hardware),
        )
        new_storage_controller = StorageController(
            name="SATA",
            type_value="AHCI",
            port_count=1,
            use_host_iocache=False,
            bootable=True,
            ide0_master_emulation_port=0,
            ide0_slave_emulation_port=1,
            ide1_master_emulation_port=2,
            ide1_slave_emulation_port=3,
            # attached_device=""
        )
        new_storage_controller.attached_device.append(AttachedDevice(
            type_value="HardDisk",
            hotpluggable=False,
            port=0,
            device=0,
            image=Image(
                uuid=os.path.basename(vdi_file).replace(".vdi", "")
            )
        ))

        self.machine.snapshot = ini_snapshot

        last_snapshot = ini_snapshot

        for save_file in save_files:
            save_file_date = save_file.replace('.sav', '')
            temp_snapshot = Snapshot(
                uuid="{" + str(uuid.uuid4()) + "}",
                name="SnapShot := {0}".format(save_file_date),
                time_stamp=save_file_date,
                # state_file=X,
                hardware=copy_hardware,
            )

            if save_file == save_files[-1]:  # LAST ITERATION
                self.machine.current_snapshot = temp_snapshot.uuid

                new_storage_controller = StorageController(
                    name="SATA",
                    type_value="AHCI",
                    port_count=1,
                    use_host_iocache=False,
                    bootable=True,
                    ide0_master_emulation_port=0,
                    ide0_slave_emulation_port=1,
                    ide1_master_emulation_port=2,
                    ide1_slave_emulation_port=3,
                    # attached_device=""
                )
                new_storage_controller.attached_device.append(AttachedDevice(
                    type_value="HardDisk",
                    hotpluggable=False,
                    port=0,
                    device=0,
                    image=Image(
                        uuid=os.path.basename(vdi_file).replace(".vdi", "")
                    )
                ))

                temp_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller
                self.machine.current_snapshot = temp_snapshot.uuid
                last_snapshot.snapshots = Snapshots(
                    snapshot=[temp_snapshot]
                )

                last_snapshot = temp_snapshot
            else:
                last_snapshot.snapshots = Snapshots(
                    [temp_snapshot]
                )
                last_snapshot = temp_snapshot

        self.machine.media_registry.hard_disks.hard_disk.hard_disk = HardDisk(
            uuid=os.path.basename(vdi_file).replace(".vdi", ""),
            location=vdi_file,
            format="vdi"
        )
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        og_config_string = serializer.render(self)
        return

    VirtualBox.add_snapshot = add_snapshot

"""
https://xsdata.readthedocs.io/en/latest/
"""

class vb(VirtualBox):
    def __init__(self,
        vboxPath:str=None,
        vboxmanage:str="VBoxManage",
        vmname = "takenname",
        username = None,
        ovafile = None,
        disablehosttime = True,
        disablenetwork = True,
        biosoffset = None,
        vmdate = None,
        network = False,
        cpu = 2,
        ram = 4096,
        sharedfolder = None,
        uploadfiles = [],
        vb_path = None,
        headless = True,
    ):
        self.vboxPath = vboxPath
        box = None
        if vboxPath is None:
            box = self.from_xml(vboxPath)
            box.vboxmanage = vboxmanage
            box.machine.name = vmname
            box.username = username
            box.machine.hardware.cpu = cpu
            box.machine.hardware.memory = ram
            box.sharedfolder = sharedfolder
            box.uploadfiles = uploadfiles
            box.vb_path = vb_path
            box.disablehosttime = disablehosttime
            box.disablenetwork = disablenetwork
            box.biosoffset = biosoffset
            box.vmdate = vmdate
            box.network = network
            box.headless = headless
            box.ovafile = ovafile
        else:
            self.vboxmanage = vboxmanage
            self.machine.name = vmname
            self.username = username
            self.machine.hardware.cpu = cpu
            self.machine.hardware.memory = ram
            self.sharedfolder = sharedfolder
            self.uploadfiles = uploadfiles
            self.vb_path = vb_path
            self.disablehosttime = disablehosttime
            self.disablenetwork = disablenetwork
            self.biosoffset = biosoffset
            self.vmdate = vmdate
            self.network = network
            self.headless = headless
            self.ovafile = ovafile

    def xml(self):
        #https://xsdata.readthedocs.io/en/latest/xml.html#serialize-xml-to-string
        from xsdata.formats.dataclass.serializers import XmlSerializer
        from xsdata.formats.dataclass.serializers.config import SerializerConfig

        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        return serializer.render(self)

    @staticmethod
    def from_xml(filename:str):
        #https://xsdata.readthedocs.io/en/latest/xml.html#parse-from-xml-filename
        from xsdata.formats.dataclass.context import XmlContext
        from xsdata.formats.dataclass.parsers import XmlParser

        parser = XmlParser(context=XmlContext())
        return parser.parse(filename, vb)

    @staticmethod
    def from_xpiz(filename:str, tempPath='/tmp/'):
        if not filename.endswith(".py"):
            return None
        
        import importlib
        controller = importlib.import_module(filename)
        zip_path = controller.download()
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
		    zip_ref.extractall(os.path.join(tempPath,zip_path))
        os.remove(zip_path)
        return os.path.join(tempPath,zip_path)


    def refresh(self):
        return vb(
            vboxPath = self.vboxPath,
            vboxmanage = self.vboxmanage,
            vmname = self.machine.name,
            username = self.username,
            disablehosttime = self.disablehosttime,
            disablenetwork = self.network,
            biosoffset = self.biosoffset,
            vmdate = self.vmdate,
            network = self.disablenetwork,
            cpu = self.machine.hardware.cpu,
            ram = self.machine.hardware.memory,
            sharedfolder = self.sharedfolder,
            uploadfiles = self.uploadfiles,
            vb_path = self.vb_path,
            headless = self.headless,
            ovafile = self.ovafile,
        )

    def on(self, headless: bool = True):
        cmd = "{0} startvm {1}".format(self.vboxmanage, self.machine.name)
        if self.headless:
            cmd += " --type headless"

        mystring.string(cmd).exec()

    def vbexe(self, cmd):
        string = "{0} guestcontrol {1} run ".format(self.vboxmanage, self.machine.name)

        if self.username:
            string += " --username {0} ".format(self.username)

        string += str(" --exe \"C:\\Windows\\System32\\cmd.exe\" -- cmd.exe/arg0 /C '" + cmd.replace("'", "\'") + "'")
        mystring.string(string).exec()

    def snapshot_take(self, snapshotname):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} take {2}".format(self.vboxmanage, self.machine.name, snapshotname)).exec()

    def snapshot_load(self, snapshotname):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} restore {2}".format(self.vboxmanage, self.machine.name, snapshotname)).exec()

    def snapshot_list(self):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} list".format(self.vboxmanage, self.machine.name)).exec()

    def snapshot_delete(self, snapshotname):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} delete {2}".format(self.vboxmanage, self.machine.name, snapshotname)).exec()

    def export_to_ova(self, ovaname):
        # https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
        mystring.string(
            "{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage, self.machine.name,ovaname)).exec()

    def __shared_folder(self, folder):
        mystring.string("{0}  sharedfolder add {1} --name \"{1}_SharedFolder\" --hostpath \"{2}\" --automount".format(
            self.vboxmanage, self.machine.name, folder)).exec()

    def add_snapshot_folder(self, snapshot_folder):
        if False and self.vboxPath:
            import datetime, uuid
            from copy import deepcopy as dc
            from pathlib import Path

            # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-showvminfo.html
            # VBoxManage showvminfo <X> --machinereadable

            parser = XmlParser()
            og_config = parser.from_path(Path(config_file), vb_struct.VirtualBox)

            # Fix the VMDK Potential
            save_files, vdi_file = [], None
            vmdk_files = []
            for filename in os.scandir(snapshot_folder):
                if os.path.isfile(filename.path):
                    if filename.name.endswith('.sav'):
                        save_files += [filename.path]
                    if filename.name.endswith('.vdi'):
                        vdi_file = filename.path
                    if filename.name.endswith('.vmdk'):
                        vmdk_files += [filename.path]
                print(filename.name)
            print(vdi_file)

            """
            VDI located in StorageControllers-attachedDevice-Image (uuid):> {06509f60-d51f-4ce4-97ed-f83cff79d93e}
            Also located in Machine -> MediaRegistry -> HardDisks -> HardDisk
            """

            # https://www.tutorialspoint.com/How-to-sort-a-Python-date-string-list
            save_files.sort(key=lambda date: datetime.datetime.strptime(
                '-'.join(date.replace('Snapshots/', '').replace('.sav', '').split("-")[:-1]), "%Y-%m-%dT%H-%M-%S"))

            copy_hardware = dc(og_config.machine.hardware)
            # save_files.reverse()
            ini_snapshot = vb_struct.Snapshot(
                uuid="{" + str(uuid.uuid4()) + "}",
                name="SnapShot := 0",
                # time_stamp=save_file_date,
                # state_file=X,
                hardware=copy_hardware,
            )

            new_storage_controller = vb_struct.StorageController(
                name="SATA",
                type="AHCI",
                port_count=1,
                use_host_iocache=False,
                bootable=True,
                ide0_master_emulation_port=0,
                ide0_slave_emulation_port=1,
                ide1_master_emulation_port=2,
                ide1_slave_emulation_port=3,
                # attached_device=""
            )
            new_storage_controller.attached_device.append(vb_struct.AttachedDevice(
                type="HardDisk",
                hotpluggable=False,
                port=0,
                device=0,
                image=vb_struct.Image(
                    uuid=os.path.basename(vdi_file).replace(".vdi", "")
                )
            ))
            # ini_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller

            # og_config.machine.current_snapshot = ini_snapshot.uuid
            og_config.machine.snapshot = ini_snapshot

            last_snapshot = ini_snapshot

            for save_file in save_files:
                save_file_date = save_file.replace('.sav', '')
                temp_snapshot = vb_struct.Snapshot(
                    uuid="{" + str(uuid.uuid4()) + "}",
                    name="SnapShot := {0}".format(save_file_date),
                    time_stamp=save_file_date,
                    # state_file=X,
                    hardware=copy_hardware,
                )

                if save_file == save_files[-1]:  # LAST ITERATION
                    og_config.machine.current_snapshot = temp_snapshot.uuid

                    new_storage_controller = vb_struct.StorageController(
                        name="SATA",
                        type="AHCI",
                        port_count=1,
                        use_host_iocache=False,
                        bootable=True,
                        ide0_master_emulation_port=0,
                        ide0_slave_emulation_port=1,
                        ide1_master_emulation_port=2,
                        ide1_slave_emulation_port=3,
                        # attached_device=""
                    )
                    new_storage_controller.attached_device.append(vb_struct.AttachedDevice(
                        type="HardDisk",
                        hotpluggable=False,
                        port=0,
                        device=0,
                        image=vb_struct.Image(
                            uuid=os.path.basename(vdi_file).replace(".vdi", "")
                        )
                    ))

                    temp_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller
                    og_config.machine.current_snapshot = temp_snapshot.uuid
                    last_snapshot.snapshots = vb_struct.Snapshots(
                        snapshot=[temp_snapshot]
                    )

                    last_snapshot = temp_snapshot
                else:
                    last_snapshot.snapshots = vb_struct.Snapshots(
                        [temp_snapshot]
                    )
                    last_snapshot = temp_snapshot

            og_config.machine.media_registry.hard_disks.hard_disk.hard_disk = vb_struct.HardDisk(
                uuid=os.path.basename(vdi_file).replace(".vdi", ""),
                location=vdi_file,
                format="vdi"
            )
            config = SerializerConfig(pretty_print=True)
            serializer = XmlSerializer(config=config)
            og_config_string = serializer.render(og_config)

            for remove, replacewith in [
                ('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ', None),
                (' xsi:type="ns0:Snapshot"', None),
                ('<ns0:', '<'),
                ('</ns0:', '</'),
                ('xmlns:ns0', 'xmlns'),
            ]:
                og_config_string = og_config_string.replace(remove, replacewith or '')

            os.system("cp {0} {0}.OG".format(config_file))
            with open(config_file, "w+") as writer:
                writer.write(og_config_string)

    def import_ova(self, ovafile):
        self.ovafile = ovafile

        mystring.string("{0}  import {1} --vsys 0 --vmname {2} --ostype \"Windows10\" --cpus {3} --memory {4}".format(
            self.vboxmanage, self.ovafile, self.machine.name, self.machine.hardware.cpu, self.machine.hardware.memory)).exec()
    
    def disableHostTime(self):
       if self.disablehosttime:
            mystring.string("{0} setextradata {1} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(
                self.vboxmanage, self.machine.name)).exec()

            self = vb.refresh()
            self.machine.extra_data.extra_data_item += ExtraDataItem(name="VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled", value="1")

    def setBiosOffset(self):
        if self.biosoffset:
            mystring.string("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.machine.name,
                                                                                 self.biosoffset)).exec()
            if False:
                self:vb
                self = vb.refresh()
                #self.machine.extra_data.extra_data_item += ExtraDataItem(name="VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled", value="1")
    
    def setVMDate(self):
        if self.vmdate:
            ms = round((self.vmdate - datetime.now().date()).total_seconds() * 1000)

            mystring.string(
                "{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.machine.name, ms)).exec()
    
    def disableNetwork(self):
        mystring.string("{0} modifyvm {1} --nic1 null".format(self.vboxmanage, self.machine.name)).exec()

    def enableNetwork(self):
        mystring.string("{0} modifyvm {1} --nic1 nat".format(self.vboxmanage, self.machine.name)).exec()

    def disable(self):
        self.disableHostTime()
        self.setBiosOffset()
        self.setVMDate()
        self.disableHostTime()

    def prep(self):
        if self.ovafile:
            self.import_ova(self.ovafile)

        self.disable()
        if self.sharedfolder:
            self.__shared_folder(self.sharedfolder)

        for file in list(self.uploadfiles):
            self.uploadfile(file)

        if False:
            self.start()
            for cmd in self.cmds_to_exe_with_network:
                self.vbexe(cmd)

            self.disableNetwork()
            # Disable the Network
            for cmd in self.cmds_to_exe_without_network:
                self.vbexe(cmd)

            # Turn on the Network
            self.enableNetwork()
            self.stop()

        self.disable()

    def run(self, headless: bool = True):
        self.prep()
        self.on(headless)

    def __enter__(self):
        self.run(True)

    def off(self):
        mystring.string("{0} controlvm {1} poweroff".format(self.vboxmanage, self.machine.name)).exec()

    def __exit__(self, type, value, traceback):
        self.stop()

    def uploadfile(self, file: str):
        mystring.string(
            "{0} guestcontrol {1} copyto {2} --target-directory=c:/Users/{3}/Desktop/ --user \"{3}\"".format(
                self.vboxmanage, self.machine.name, file, self.username)).exec()

    def clean(self, deletefiles: bool = True):
        cmd = "{0} unregistervm {1}".format(self.vboxmanage, self.machine.name)

        if deletefiles:
            cmd += " --delete"
            if self.ovafile:
                os.remove(self.ovafile)

        mystring.string(cmd).exec()

    def destroy(self, deletefiles: bool = True):
        self.clean(deletefiles)
