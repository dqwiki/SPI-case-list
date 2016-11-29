"""
(C) 2016 DeltaQuad (enwp.org/User:DeltaQuad)

This file is part of DeltaQuadBot.

DeltaQuadBot is free software: you can redistribute it and/or modify
it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DeltaQuadBot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU AFFERO GENERAL PUBLIC LICENSE for more details.

You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
along with DeltaQuadBot. If not, see <https://www.gnu.org/licenses/agpl.txt>.
"""

##Main Settings
botname = "DeltaQuadBot"

##Default System Path
winpath = "C:\\pywikipedia\\core\\"#Windows path for pywikipedia, need "\\" for folder switch
linuxpath = "/data/project/deltaquad-bots/pywikipedia/core"

#Onwiki paths
waitlist = "User:DeltaQuad/UAA/Wait"
gopage = "User:DeltaQuad/UAA/Run"
timepage = "User:DeltaQuad/UAA/Time"
settings = "User:DeltaQuad/UAA/Settings"
blacklist = 'User:DeltaQuad/UAA/Blacklist'
whitelist = 'User:DeltaQuad/UAA/Whitelist'
simlist =  'User:DeltaQuad/UAA/Similar'
postpage = "Wikipedia:Usernames for administrator attention/Bot"
holdpage = "Wikipedia:Usernames for administrator attention/Holding pen"

#Runtime edit summarties
primarytaskname = "Task UAA listing"
editsumtime = "[[User:DeltaQuadBot|DeltaQuadBot]] UAA Updating Run Time."
editsumwait = "[[User:DeltaQuadBot|DeltaQuadBot]] Update UAA wait list."
editsumclear = "[[User:DeltaQuadBot|DeltaQuadBot]] UAA Removing blocked users and moving waiting requests."
