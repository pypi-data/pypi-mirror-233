# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import logging
from os import PathLike
from pathlib import Path
from majormode.perseus.utils import cast

from bootloader.constant.ue_asset import ASSET_CLASS_NAME_MAPPING
from bootloader.constant.ue_asset import UnrealEngineAssetClass
from bootloader.model.asset import Asset


class UnrealEngineAsset(Asset):
    # The default extension (suffix) of a Unreal Editor asset file.
    UNREAL_ENGINE_ASSET_FILE_EXTENSION = '.uasset'

    # The path prefix of Unreal Engine core classes.
    UNREAL_ENGINE_STANDARD_CLASS_PATH_PREFIX = '/Script/Engine/'

    # The class of an Unreal Engine asset world.
    UNREAL_ENGINE_WORLD_ASSET_CLASS = '/Script/Engine/World'

    @property
    def file_name(self) -> str:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """
        return f'{self._asset_name}.{self.UNREAL_ENGINE_ASSET_FILE_EXTENSION}'

    @property
    def file_path_name(self) -> PathLike:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """
        pathname = self._package_name.replace('Game', 'Content')
        return Path(f'{pathname}.{self.UNREAL_ENGINE_ASSET_FILE_EXTENSION}')

    def is_storable(self) -> bool:
        """
        Indicate whether this asset needs to be stored in the inventory.


        :return: ``true`` is the asset needs to be stored in the inventory;
            ``false`` otherwise.
        """
        return self._asset_class_path == '/Script/Engine/World'

    @property
    def asset_class(self) -> UnrealEngineAssetClass:
        """
        Return the asset's class.

        For example, the class of a `/Script/Engine/SkeletalMesh` asset is
        `AssetClass.SkeletalMesh`


        :return: The class of the asset, or `None` if the class is not defined
            (i.e., a user-defined class).
        """
        class_name = self._asset_class_path.split('/')[-1]
        try:
            asset_class = cast.string_to_enum(class_name, UnrealEngineAssetClass)
            return asset_class
        except ValueError as error:
            logging.exception(error)

    @property
    def asset_class_name(self) -> str:
        """
        Return the humanly readable name of the asset's class.

        For example, the humanly readable name of the class
        `/Script/Engine/SkeletalMesh` is `Skeletal Mesh`.


        :return: The humanly readable name of the asset's class, or ``None``
            if the asset's class doesn't correspond to an Unreal Engine
            standard class.
        """
        asset_class_name = ASSET_CLASS_NAME_MAPPING.get(self.asset_class)
        if asset_class_name is None and self.has_standard_class():
            logging.warning(
                f"The Unreal Engine class {self.asset_class} might not be properly "
                f"declared in the enumeration 'UnrealEngineAssetClass'"
            )
        return asset_class_name

    def has_standard_class(self):
        """
        Indicate whether this asset has a standard Unreal Engine class.

        Developers can create their own Unreal Engine classes such as
        ``/Script/ControlRigDeveloper/ControlRigBlueprint``, or even more
        specific to their game, such as ``/Game/Scooby/D_ARSessionConfig``.

        Unreal Engine classes are prefixed with ``/Script/Engine/``.


        :return: ``True`` if this asset has a standard Unreal Engine class;
            ``False`` if this asset has a custom class.
        """
        return self.asset_class_path.startswith(self.UNREAL_ENGINE_STANDARD_CLASS_PATH_PREFIX)


# class UnrealEngineAbstractAssetFile:
#     def __eq__(self, other: UnrealEngineAbstractAssetFile):
#         """
#         Check whether this asset is the same as another asset.
#
#         Two assets are equivalent if they have the same name, the same class,
#         the same package name, and the same file's checksum.
#
#
#         :param other: Another asset.
#
#
#         :return: ``True`` if the two assets are the same; ``False`` otherwise.
#         """
#         return other is not None \
#             and self.file_checksum == other.file_checksum \
#             and self.__asset == other.asset
#
#     def __init__(
#             self,
#             asset: UnrealEngineAsset):
#         """
#         Build a new {@link UAsset}.
#         """
#         self.__asset = asset
#
#     def __str__(self):
#         """
#         Return the string representation of this asset file.
#
#
#         :return: Return a stringified JSON expression of this asset file.
#         """
#         return json.dumps(obj.stringify(self.to_json(), trimmable=True))
#
#     @property
#     def asset(self) -> UnrealEngineAsset:
#         """
#         Return the information of the asset contained in this file.
#
#
#         :return: An asset.
#         """
#         return self.__asset
#
#     @property
#     @abstractmethod
#     def file_checksum(self) -> str:
#         """
#         Return the SHA256 message digest of the binary data of the asset file.
#
#
#         :return: The SHA256 message digest of the binary data of the asset
#             file.
#         """
#         pass
#
#     @property
#     @abstractmethod
#     def file_size(self) -> int:
#         """
#         Return the size of the asset file.
#
#
#         :return: The size in bytes of the asset file.
#         """
#         pass
#
#     def to_json(self) -> any:
#         """
#         Serialize the asset file's information to a JSON expression.
#
#
#         :return: A JSON expression representing the asset file's information.
#         """
#         payload = self.__asset.to_json()
#         payload['file_size'] = self.file_size
#         payload['file_checksum'] = self.file_checksum
#         return payload
#
#
# class UnrealEngineRecordAssetFile(UnrealEngineAbstractAssetFile):
#     """
#     Represent the information of an asset as registered in a database.
#     """
#     def __init__(
#             self,
#             asset: UnrealEngineAsset,
#             file_size: int,
#             file_checksum: str):
#         """
#         :param asset:
#
#         :param file_checksum: The SHA256 message digest of the binary data of
#             the asset file.
#
#         """
#         super().__init__(asset)
#         self.__file_checksum = file_checksum
#         self.__file_size = file_size
#
#     @property
#     def file_checksum(self) -> str:
#         """
#         Return the SHA256 message digest of the binary data of the asset file.
#
#
#         :return: The SHA256 message digest of the binary data of the asset
#             file.
#         """
#         return self.__file_checksum
#
#     @file_checksum.setter
#     def file_checksum(self, file_checksum: str):
#         """
#         Set the SHA256 message digest of the binary data of the asset file
#         when its content has changed.
#
#
#         :param file_checksum: The SHA256 message digest of the binary data of
#             the asset file.
#         """
#         logging.debug(
#             f"The checksum of the asset file {self.asset.asset_name} has changed "
#             f"from the value {self.__file_checksum} to the value {file_checksum}"
#         )
#         self.__file_checksum = file_checksum
#
#     @property
#     def file_size(self) -> int:
#         """
#         Return the size of the asset file.
#
#
#         :return: The size in bytes of the asset file.
#         """
#         return self.__file_size
#
#     @file_size.setter
#     def file_size(self, file_size: int):
#         """
#         Set the size of the asset file when its content has changed.
#
#
#         :param file_size: The size in bytes of the asset file.
#         """
#         logging.debug(
#             f"The size of the asset file {self.asset.asset_name} has changed "
#             f"from the value {self.__file_size} to the value {file_size}"
#         )
#         self.__file_size = file_size
#
#     @staticmethod
#     def from_json(payload: any) -> UnrealEngineRecordAssetFile:
#         """
#         Return an asset as stored in a database record.
#
#         :param payload: The JSON data of the asset.
#
#
#         :return: An asset.
#         """
#         asset = UnrealEngineAsset.from_json(payload)
#         return UnrealEngineRecordAssetFile(
#             asset,
#             payload['file_size'],
#             payload['file_checksum']
#         )
#
#
# class UnrealEngineRealAssetFile(UnrealEngineAbstractAssetFile):
#     """
#     Represent the file of an asset stored on the file system.
#     """
#     FILE_READ_BLOCK_SIZE = 4096
#
#     def __init__(
#             self,
#             asset: UnrealEngineAsset,
#             file_path_name: Path):
#         super().__init__(asset)
#
#         if not os.path.exists(file_path_name):
#             error_message = f"The file {file_path_name} of the asset {asset.asset_name} doesn't exist"
#             logging.error(error_message)
#             raise FileNotFoundError(error_message)
#
#         file_status = Path.stat(file_path_name)
#         self.__file_size = file_status.st_size
#
#         self.__asset = asset
#         self.__file_path_name = file_path_name
#         self.__file_checksum = None  # This attribute is lazy loaded (cf. property `file_checksum`)
#
#     def __calculate_file_checksum(self) -> str:
#         """
#         Calculate the SHA256 message digest of the binary data of the asset
#         file.
#
#
#         :return: The SHA256 message digest of the binary data of the asset
#             file.
#         """
#         sha256_hash = hashlib.sha256()
#
#         with open(self.__file_path_name, 'rb') as fd:
#             # Read and update hash string value in blocks of bytes.
#             for byte_block in iter(lambda: fd.read(self.FILE_READ_BLOCK_SIZE), b''):
#                 sha256_hash.update(byte_block)
#
#         return sha256_hash.hexdigest()
#
#     @property
#     def file_checksum(self) -> str:
#         """
#         Return the SHA256 message digest of the binary data of the asset file.
#
#
#         :return: The SHA256 message digest of the binary data of the asset
#             file.
#         """
#         if self.__file_checksum is None:
#             self.__file_checksum = self.__calculate_file_checksum()
#
#         return self.__file_checksum
#
#     @property
#     def file_path_name(self) -> Path:
#         """
#         Return the path and name of the asset's file.
#
#
#         :return: The path and name of the asset's file.
#         """
#         return self.__file_path_name
#
#     @property
#     def file_size(self) -> int:
#         """
#         Return the size of the asset file.
#
#
#         :return: The size in bytes of the asset file.
#         """
#         return self.__file_size
