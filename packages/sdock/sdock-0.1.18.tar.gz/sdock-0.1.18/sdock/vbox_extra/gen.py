from dataclasses import dataclass, field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime


__NAMESPACE__ = "http://www.virtualbox.org/"


@dataclass(order=True, unsafe_hash=True)
class AudioAdapter:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    controller: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    driver: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    enabled_out: Optional[bool] = field(
        default=None,
        metadata={
            "name": "enabledOut",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Clipboard:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    mode: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Controller:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Display:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    controller: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    vramsize: Optional[int] = field(
        default=None,
        metadata={
            "name": "VRAMSize",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class DragAndDrop:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    mode: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class ExtraDataItem:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[Union[int, bool, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class GuestProperty:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[Union[int, str, bool]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    timestamp: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    flags: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Hid:
    class Meta:
        name = "HID"
        namespace = "http://www.virtualbox.org/"

    pointing: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pointing",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class HardDisk:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    hard_disk: Optional["HardDisk"] = field(
        default=None,
        metadata={
            "name": "HardDisk",
            "type": "Element",
        }
    )


@dataclass(order=True, unsafe_hash=True)
class HardwareVirtExLargePages:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Ioapic:
    class Meta:
        name = "IOAPIC"
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Image:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(order=True, unsafe_hash=True)
class LongMode:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Memory:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    ramsize: Optional[int] = field(
        default=None,
        metadata={
            "name": "RAMSize",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Nat:
    class Meta:
        name = "NAT"
        namespace = "http://www.virtualbox.org/"

    localhost_reachable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "localhost-reachable",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Pae:
    class Meta:
        name = "PAE"
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class SharedFolder:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    host_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "hostPath",
            "type": "Attribute",
            "required": True,
        }
    )
    writable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    auto_mount: Optional[bool] = field(
        default=None,
        metadata={
            "name": "autoMount",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class SmbiosUuidLittleEndian:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Snapshots:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    snapshot: Optional["Snapshot"] = field(
        default=None,
        metadata={
            "name": "Snapshot",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Adapter:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    slot: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    macaddress: Optional[str] = field(
        default=None,
        metadata={
            "name": "MACAddress",
            "type": "Attribute",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    nat: Optional[Nat] = field(
        default=None,
        metadata={
            "name": "NAT",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class AttachedDevice:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    passthrough: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    hotpluggable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    port: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    device: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    image: Optional[Image] = field(
        default=None,
        metadata={
            "name": "Image",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Bios:
    class Meta:
        name = "BIOS"
        namespace = "http://www.virtualbox.org/"

    ioapic: Optional[Ioapic] = field(
        default=None,
        metadata={
            "name": "IOAPIC",
            "type": "Element",
            "required": True,
        }
    )
    smbios_uuid_little_endian: Optional[SmbiosUuidLittleEndian] = field(
        default=None,
        metadata={
            "name": "SmbiosUuidLittleEndian",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Cpu:
    class Meta:
        name = "CPU"
        namespace = "http://www.virtualbox.org/"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    pae: Optional[Pae] = field(
        default=None,
        metadata={
            "name": "PAE",
            "type": "Element",
            "required": True,
        }
    )
    long_mode: Optional[LongMode] = field(
        default=None,
        metadata={
            "name": "LongMode",
            "type": "Element",
            "required": True,
        }
    )
    hardware_virt_ex_large_pages: Optional[HardwareVirtExLargePages] = field(
        default=None,
        metadata={
            "name": "HardwareVirtExLargePages",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Controllers:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    controller: Optional[Controller] = field(
        default=None,
        metadata={
            "name": "Controller",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Dvdimages:
    class Meta:
        name = "DVDImages"
        namespace = "http://www.virtualbox.org/"

    image: Optional[Image] = field(
        default=None,
        metadata={
            "name": "Image",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class ExtraData:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    extra_data_item: List[ExtraDataItem] = field(
        default_factory=list,
        metadata={
            "name": "ExtraDataItem",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class GuestProperties:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    guest_property: List[GuestProperty] = field(
        default_factory=list,
        metadata={
            "name": "GuestProperty",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class HardDisks:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    hard_disk: Optional[HardDisk] = field(
        default=None,
        metadata={
            "name": "HardDisk",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class SharedFolders:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    shared_folder: Optional[SharedFolder] = field(
        default=None,
        metadata={
            "name": "SharedFolder",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class MediaRegistry:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    hard_disks: Optional[HardDisks] = field(
        default=None,
        metadata={
            "name": "HardDisks",
            "type": "Element",
            "required": True,
        }
    )
    dvdimages: Optional[Dvdimages] = field(
        default=None,
        metadata={
            "name": "DVDImages",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Network:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    adapter: Optional[Adapter] = field(
        default=None,
        metadata={
            "name": "Adapter",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class StorageController:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    port_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PortCount",
            "type": "Attribute",
            "required": True,
        }
    )
    use_host_iocache: Optional[bool] = field(
        default=None,
        metadata={
            "name": "useHostIOCache",
            "type": "Attribute",
            "required": True,
        }
    )
    bootable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Bootable",
            "type": "Attribute",
            "required": True,
        }
    )
    ide0_master_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE0MasterEmulationPort",
            "type": "Attribute",
            "required": True,
        }
    )
    ide0_slave_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE0SlaveEmulationPort",
            "type": "Attribute",
            "required": True,
        }
    )
    ide1_master_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE1MasterEmulationPort",
            "type": "Attribute",
            "required": True,
        }
    )
    ide1_slave_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE1SlaveEmulationPort",
            "type": "Attribute",
            "required": True,
        }
    )
    attached_device: List[AttachedDevice] = field(
        default_factory=list,
        metadata={
            "name": "AttachedDevice",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Usb:
    class Meta:
        name = "USB"
        namespace = "http://www.virtualbox.org/"

    controllers: Optional[Controllers] = field(
        default=None,
        metadata={
            "name": "Controllers",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class StorageControllers:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    storage_controller: Optional[StorageController] = field(
        default=None,
        metadata={
            "name": "StorageController",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Hardware:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    cpu: Optional[Cpu] = field(
        default=None,
        metadata={
            "name": "CPU",
            "type": "Element",
            "required": True,
        }
    )
    memory: Optional[Memory] = field(
        default=None,
        metadata={
            "name": "Memory",
            "type": "Element",
            "required": True,
        }
    )
    hid: Optional[Hid] = field(
        default=None,
        metadata={
            "name": "HID",
            "type": "Element",
            "required": True,
        }
    )
    display: Optional[Display] = field(
        default=None,
        metadata={
            "name": "Display",
            "type": "Element",
            "required": True,
        }
    )
    bios: Optional[Bios] = field(
        default=None,
        metadata={
            "name": "BIOS",
            "type": "Element",
            "required": True,
        }
    )
    usb: Optional[Usb] = field(
        default=None,
        metadata={
            "name": "USB",
            "type": "Element",
            "required": True,
        }
    )
    network: Optional[Network] = field(
        default=None,
        metadata={
            "name": "Network",
            "type": "Element",
            "required": True,
        }
    )
    audio_adapter: Optional[AudioAdapter] = field(
        default=None,
        metadata={
            "name": "AudioAdapter",
            "type": "Element",
            "required": True,
        }
    )
    shared_folders: Optional[SharedFolders] = field(
        default=None,
        metadata={
            "name": "SharedFolders",
            "type": "Element",
            "required": True,
        }
    )
    clipboard: Optional[Clipboard] = field(
        default=None,
        metadata={
            "name": "Clipboard",
            "type": "Element",
            "required": True,
        }
    )
    drag_and_drop: Optional[DragAndDrop] = field(
        default=None,
        metadata={
            "name": "DragAndDrop",
            "type": "Element",
            "required": True,
        }
    )
    guest_properties: Optional[GuestProperties] = field(
        default=None,
        metadata={
            "name": "GuestProperties",
            "type": "Element",
            "required": True,
        }
    )
    storage_controllers: Optional[StorageControllers] = field(
        default=None,
        metadata={
            "name": "StorageControllers",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Snapshot:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    time_stamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "timeStamp",
            "type": "Attribute",
            "required": True,
        }
    )
    state_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "stateFile",
            "type": "Attribute",
            "required": True,
        }
    )
    hardware: Optional[Hardware] = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
            "required": True,
        }
    )
    snapshots: Optional[Snapshots] = field(
        default=None,
        metadata={
            "name": "Snapshots",
            "type": "Element",
        }
    )


@dataclass(order=True, unsafe_hash=True)
class Machine:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    ostype: Optional[str] = field(
        default=None,
        metadata={
            "name": "OSType",
            "type": "Attribute",
            "required": True,
        }
    )
    state_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "stateFile",
            "type": "Attribute",
            "required": True,
        }
    )
    current_snapshot: Optional[str] = field(
        default=None,
        metadata={
            "name": "currentSnapshot",
            "type": "Attribute",
            "required": True,
        }
    )
    snapshot_folder: Optional[str] = field(
        default=None,
        metadata={
            "name": "snapshotFolder",
            "type": "Attribute",
            "required": True,
        }
    )
    current_state_modified: Optional[bool] = field(
        default=None,
        metadata={
            "name": "currentStateModified",
            "type": "Attribute",
            "required": True,
        }
    )
    last_state_change: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastStateChange",
            "type": "Attribute",
            "required": True,
        }
    )
    media_registry: Optional[MediaRegistry] = field(
        default=None,
        metadata={
            "name": "MediaRegistry",
            "type": "Element",
            "required": True,
        }
    )
    extra_data: Optional[ExtraData] = field(
        default=None,
        metadata={
            "name": "ExtraData",
            "type": "Element",
            "required": True,
        }
    )
    snapshot: Optional[Snapshot] = field(
        default=None,
        metadata={
            "name": "Snapshot",
            "type": "Element",
            "required": True,
        }
    )
    hardware: Optional[Hardware] = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True, unsafe_hash=True)
class VirtualBox:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    machine: Optional[Machine] = field(
        default=None,
        metadata={
            "name": "Machine",
            "type": "Element",
            "required": True,
        }
    )
