import { useEffect, useState } from "react";
import {
  Card,
  CardHeader,
  CardContent,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Typography,
  Box,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  IconButton,
  Snackbar,
  Alert,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import type { Email, EmailCategory } from "../api/emails";
import { listEmails, updateEmail } from "../api/emails";

export function EmailListPage() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState<EmailCategory | "">("");
  const [onlyReview, setOnlyReview] = useState(false);

  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);
  const [detailDraft, setDetailDraft] = useState("");
  const [detailCategory, setDetailCategory] = useState<
    EmailCategory | "INCONCLUSIVO"
  >("INCONCLUSIVO");
  const [detailRequiresReview, setDetailRequiresReview] = useState(false);
  const [saving, setSaving] = useState(false);

  // Snackbar de feedback
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] =
    useState<"success" | "error">("success");

  async function fetchData() {
    try {
      setLoading(true);
      const data = await listEmails();
      setEmails(data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void fetchData();
  }, []);

  const filtered = emails.filter((email) => {
    if (category && email.category !== category) return false;
    if (onlyReview && !email.requires_human_review) return false;
    return true;
  });

  function getCategoryLabel(cat: EmailCategory) {
    switch (cat) {
      case "FEEDBACK_NEGATIVO":
        return "Feedback negativo";
      case "FEEDBACK_POSITIVO":
        return "Feedback positivo";
      case "GARANTIA":
        return "Garantia";
      case "ARREPENDIMENTO_REEMBOLSO":
        return "Arrependimento/Reembolso";
      case "DUVIDAS_GERAIS":
        return "Dúvidas gerais";
      case "INCONCLUSIVO":
      default:
        return "Inconclusivo";
    }
  }

  function categoryColor(cat: EmailCategory) {
    switch (cat) {
      case "FEEDBACK_NEGATIVO":
        return "error";
      case "FEEDBACK_POSITIVO":
        return "success";
      case "GARANTIA":
        return "warning";
      case "ARREPENDIMENTO_REEMBOLSO":
        return "info";
      case "DUVIDAS_GERAIS":
        return "primary";
      case "INCONCLUSIVO":
      default:
        return "default";
    }
  }

  function openDetails(email: Email) {
    setSelectedEmail(email);
    setDetailDraft(email.draft_reply);
    setDetailCategory(email.category ?? "INCONCLUSIVO");
    setDetailRequiresReview(email.requires_human_review);
  }

  function closeDetails() {
    setSelectedEmail(null);
  }

  async function handleSave() {
    if (!selectedEmail) return;
    try {
      setSaving(true);
      const updated = await updateEmail(selectedEmail.id, {
        draft_reply: detailDraft,
        category: detailCategory,
        requires_human_review: detailRequiresReview,
      });

      // Atualiza lista em memória
      setEmails((prev) =>
        prev.map((e) => (e.id === updated.id ? updated : e)),
      );
      setSelectedEmail(updated);

      setSnackbarMessage("Alterações salvas com sucesso.");
      setSnackbarSeverity("success");
      setSnackbarOpen(true);
    } catch (error) {
      console.error(error);
      setSnackbarMessage("Erro ao salvar alterações. Tente novamente.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <Card>
        <CardHeader
          title="E-mails classificados"
          subheader="Visualize, filtre e revise e-mails processados pela IA"
        />
        <CardContent>
          <Stack spacing={2}>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
              <FormControl size="small" sx={{ minWidth: 220 }}>
                <InputLabel>Categoria</InputLabel>
                <Select
                  label="Categoria"
                  value={category}
                  onChange={(e) =>
                    setCategory(e.target.value as EmailCategory | "")
                  }
                >
                  <MenuItem value="">Todas</MenuItem>
                  <MenuItem value="FEEDBACK_NEGATIVO">
                    Feedback negativo
                  </MenuItem>
                  <MenuItem value="FEEDBACK_POSITIVO">
                    Feedback positivo
                  </MenuItem>
                  <MenuItem value="GARANTIA">Garantia</MenuItem>
                  <MenuItem value="ARREPENDIMENTO_REEMBOLSO">
                    Arrependimento/Reembolso
                  </MenuItem>
                  <MenuItem value="DUVIDAS_GERAIS">Dúvidas gerais</MenuItem>
                  <MenuItem value="INCONCLUSIVO">Inconclusivo</MenuItem>
                </Select>
              </FormControl>

              <FormControlLabel
                control={
                  <Checkbox
                    checked={onlyReview}
                    onChange={(e) => setOnlyReview(e.target.checked)}
                  />
                }
                label="Somente com revisão humana"
              />
            </Stack>

            {loading && <LinearProgress />}

            {filtered.length === 0 && !loading && (
              <Typography variant="body2" color="text.secondary">
                Nenhum e-mail encontrado com os filtros atuais.
              </Typography>
            )}

            {filtered.length > 0 && (
              <Box sx={{ overflowX: "auto" }}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Remetente</TableCell>
                      <TableCell>Assunto</TableCell>
                      <TableCell>Categoria</TableCell>
                      <TableCell>Confiança</TableCell>
                      <TableCell>Revisão</TableCell>
                      <TableCell>Data</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filtered.map((email) => (
                      <TableRow
                        key={email.id}
                        hover
                        sx={{ cursor: "pointer" }}
                        onClick={() => openDetails(email)}
                      >
                        <TableCell>{email.from_email}</TableCell>
                        <TableCell>{email.subject}</TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            label={getCategoryLabel(email.category)}
                            color={categoryColor(email.category) as any}
                          />
                        </TableCell>
                        <TableCell>
                          {(email.confidence * 100).toFixed(0)}%
                        </TableCell>
                        <TableCell>
                          {email.requires_human_review ? "Sim" : "Não"}
                        </TableCell>
                        <TableCell>
                          {new Date(email.created_at).toLocaleString("pt-BR")}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Box>
            )}
          </Stack>
        </CardContent>
      </Card>

      {/* Dialog de detalhes */}
      <Dialog
        open={!!selectedEmail}
        onClose={closeDetails}
        fullWidth
        maxWidth="md"
      >
        <DialogTitle sx={{ pr: 6 }}>
          Detalhes do e-mail
          <IconButton
            aria-label="close"
            onClick={closeDetails}
            sx={{ position: "absolute", right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        {selectedEmail && (
          <DialogContent dividers>
            <Stack spacing={2}>
              <Typography variant="subtitle2">Remetente</Typography>
              <Typography>{selectedEmail.from_email}</Typography>

              <Typography variant="subtitle2">Assunto</Typography>
              <Typography>{selectedEmail.subject}</Typography>

              <Typography variant="subtitle2">Corpo do e-mail</Typography>
              <Box
                sx={{
                  p: 1,
                  border: "1px solid #e5e7eb",
                  borderRadius: 1,
                  bgcolor: "#f9fafb",
                  maxHeight: 200,
                  overflowY: "auto",
                  whiteSpace: "pre-wrap",
                }}
              >
                {selectedEmail.body}
              </Box>

              <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
                <FormControl size="small" sx={{ minWidth: 220 }}>
                  <InputLabel>Categoria</InputLabel>
                  <Select
                    label="Categoria"
                    value={detailCategory}
                    onChange={(e) =>
                      setDetailCategory(
                        e.target.value as EmailCategory | "INCONCLUSIVO",
                      )
                    }
                  >
                    <MenuItem value="FEEDBACK_NEGATIVO">
                      Feedback negativo
                    </MenuItem>
                    <MenuItem value="FEEDBACK_POSITIVO">
                      Feedback positivo
                    </MenuItem>
                    <MenuItem value="GARANTIA">Garantia</MenuItem>
                    <MenuItem value="ARREPENDIMENTO_REEMBOLSO">
                      Arrependimento/Reembolso
                    </MenuItem>
                    <MenuItem value="DUVIDAS_GERAIS">
                      Dúvidas gerais
                    </MenuItem>
                    <MenuItem value="INCONCLUSIVO">Inconclusivo</MenuItem>
                  </Select>
                </FormControl>

                <FormControlLabel
                  control={
                    <Checkbox
                      checked={detailRequiresReview}
                      onChange={(e) =>
                        setDetailRequiresReview(e.target.checked)
                      }
                    />
                  }
                  label="Manter marcado para revisão humana"
                />
              </Stack>

              <Typography variant="subtitle2">Confiança do modelo</Typography>
              <Typography>
                {(selectedEmail.confidence * 100).toFixed(0)}%
              </Typography>

              <Typography variant="subtitle2">Rascunho de resposta</Typography>
              <TextField
                value={detailDraft}
                onChange={(e) => setDetailDraft(e.target.value)}
                multiline
                minRows={5}
                fullWidth
              />
            </Stack>
          </DialogContent>
        )}
        <DialogActions>
          <Button onClick={closeDetails}>Fechar</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={saving || !selectedEmail}
          >
            {saving ? "Salvando..." : "Salvar alterações"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar de feedback */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      >
        <Alert
          onClose={() => setSnackbarOpen(false)}
          severity={snackbarSeverity}
          sx={{ width: "100%" }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
}