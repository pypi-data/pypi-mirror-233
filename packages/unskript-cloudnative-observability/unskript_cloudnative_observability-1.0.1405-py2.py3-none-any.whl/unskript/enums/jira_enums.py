##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from unskript.enums.enum_by_name import EnumByName
import enum


@enum.unique
class IssueType(str, EnumByName):
    BUG = "Bug"
    TASK = "Task"
    STORY = "Story"
    EPIC = "Epic"

