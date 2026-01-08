// src/components/AppLayout.tsx
import { useState, type ReactNode } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Tabs,
  Tab,
  Box,
} from "@mui/material";
import MailOutlineIcon from "@mui/icons-material/MailOutline";
import ListAltIcon from "@mui/icons-material/ListAlt";

interface AppLayoutProps {
  classifyPage: ReactNode;
  listPage: ReactNode;
}

export function AppLayout({ classifyPage, listPage }: AppLayoutProps) {
  const [tab, setTab] = useState<"classify" | "list">("classify");

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f3f4f6" }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <MailOutlineIcon sx={{ mr: 1 }} />
          <Typography variant="h6">Email Assistant - Dashboard</Typography>
        </Toolbar>
      </AppBar>

      <Box sx={{ borderBottom: 1, borderColor: "divider", bgcolor: "background.paper" }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} centered>
          <Tab
            label="Classificar e-mail"
            value="classify"
            icon={<MailOutlineIcon />}
            iconPosition="start"
          />
          <Tab
            label="E-mails classificados"
            value="list"
            icon={<ListAltIcon />}
            iconPosition="start"
          />
        </Tabs>
      </Box>

      {/* Conteúdo centralizado, mas ocupando bem a largura */}
      <Box
        sx={{
          width: "100%",
          maxWidth: "1600px",
          margin: "0 auto",
          px: 3,
          py: 3,
        }}
      >
        {tab === "classify" ? classifyPage : listPage}
      </Box>
    </Box>
  );
}