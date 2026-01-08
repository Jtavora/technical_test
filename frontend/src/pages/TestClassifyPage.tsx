import type { FormEvent } from "react";
import { useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  TextField,
  Button,
  Stack,
  Typography,
  Alert,
  CircularProgress,
  Box,
} from "@mui/material";
import type { Email } from "../api/emails";
import { classifyEmail } from "../api/emails";

export function TestClassifyPage() {
  const [fromEmail, setFromEmail] = useState("cliente@example.com");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Email | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await classifyEmail({
        from_email: fromEmail,
        subject,
        body,
      });
      setResult(data);
    } catch {
      setError("Erro ao classificar o e-mail. Verifique se a API está acessível.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Stack spacing={3}>
      <Card>
        <CardHeader title="Classificar novo e-mail" />
        <CardContent>
          <Box component="form" onSubmit={handleSubmit}>
            <Stack spacing={2}>
              <TextField
                label="Remetente"
                type="email"
                value={fromEmail}
                onChange={(e) => setFromEmail(e.target.value)}
                fullWidth
                required
              />
              <TextField
                label="Assunto"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                fullWidth
                required
              />
              <TextField
                label="Corpo do e-mail"
                value={body}
                onChange={(e) => setBody(e.target.value)}
                fullWidth
                required
                multiline
                minRows={5}
              />

              <Box>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  startIcon={
                    loading ? <CircularProgress size={18} color="inherit" /> : undefined
                  }
                >
                  {loading ? "Classificando..." : "Classificar"}
                </Button>
              </Box>

              {error && <Alert severity="error">{error}</Alert>}
            </Stack>
          </Box>
        </CardContent>
      </Card>

      {result && (
        <Card>
          <CardHeader title="Resultado da classificação" />
          <CardContent>
            <Stack spacing={1.5}>
              <Typography>
                <strong>Categoria:</strong> {result.category}
              </Typography>
              <Typography>
                <strong>Confiança:</strong> {(result.confidence * 100).toFixed(0)}%
              </Typography>
              <Typography>
                <strong>Revisão humana?</strong>{" "}
                {result.requires_human_review ? "Sim" : "Não"}
              </Typography>

              <Box mt={2}>
                <Typography fontWeight={600} mb={1}>
                  Rascunho sugerido:
                </Typography>
                <TextField
                  value={result.draft_reply}
                  fullWidth
                  multiline
                  minRows={5}
                />
              </Box>
            </Stack>
          </CardContent>
        </Card>
      )}
    </Stack>
  );
}