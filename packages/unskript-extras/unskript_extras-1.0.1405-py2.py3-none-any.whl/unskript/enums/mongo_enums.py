##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from unskript.enums.enum_by_name import EnumByName
import enum


@enum.unique
class FindCommands(str, EnumByName):
    find = 'find'
    find_one = 'find_one'
    find_one_and_delete = 'find_one_and_delete'
    find_one_and_replace = 'find_one_and_replace'
    find_one_and_update = 'find_one_and_update'


@enum.unique
class InsertCommands(str, EnumByName):
    insert_one = 'insert_one'
    insert_many = 'insert_many'

@enum.unique

class DeleteCommands(str, EnumByName):
    delete_one = 'delete_one'
    delete_many = 'delete_many'


@enum.unique
class UpdateCommands(str, EnumByName):
    update_one = 'update_one'
    update_many = 'update_many'
