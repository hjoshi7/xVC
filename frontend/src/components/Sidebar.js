import React from "react";
import "./Sidebar.css";
import SidebarOption from "./SidebarOption"
import XIcon from '@mui/icons-material/X';
import HomeIcon from '@mui/icons-material/Home';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import SearchIcon from "@mui/icons-material/Search";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import MailOutlineIcon from "@mui/icons-material/MailOutline";
import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";
import ListAltIcon from "@mui/icons-material/ListAlt";
import PermIdentityIcon from "@mui/icons-material/PermIdentity";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import { Button } from "@mui/material";

function Sidebar() {
  return (
    <div className="sidebar">
      <XIcon className="sidebar__twitterIcon" />
      <SidebarOption Icon={HomeIcon} text="Home" />
      <SidebarOption Icon={SearchIcon} text="Explore" />
      <SidebarOption Icon={NotificationsNoneIcon} text="Notifications" />
      <SidebarOption Icon={MailOutlineIcon} text="Messages" />
      <SidebarOption Icon={ShowChartIcon} text="𝕏VC" active={true}/>
      <SidebarOption Icon={ListAltIcon} text="Lists" />
      <SidebarOption Icon={BookmarkBorderIcon} text="Bookmarks" />

      <SidebarOption Icon={XIcon} text="Premium"/>
      <SidebarOption Icon={PermIdentityIcon} text="Profile" />
      <SidebarOption Icon={MoreHorizIcon} text="More" />

      <Button variant="outlined" className="sidebar__tweet" fullWidth>
        Post
      </Button>
    </div>
  );
}

export default Sidebar;
